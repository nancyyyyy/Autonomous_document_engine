from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.services.repository_service import RepositoryService
from app.domain.models.change_event import ChangeEvent
from app.core.database import get_session
from app.services.change_detector import ChangeDetector

router = APIRouter(prefix="/api/v1")


class GitHubWebhookPayload(BaseModel):
    action: str = ""
    repository: Dict[str, Any] = {}
    sender: Dict[str, Any] = {}
    commits: list = []
    pull_request: Optional[Dict[str, Any]] = None
    after: Optional[str] = None
    number: Optional[int] = None


@router.post("/webhooks/github")
async def github_webhook(
    payload: GitHubWebhookPayload,
    background_tasks: BackgroundTasks
):
    """Main Webhook Handler"""
    
    repo_data = payload.repository
    repo_full_name = repo_data.get("full_name", "unknown")
    event_type = "push" if payload.commits else "pull_request"
    
    print(f"📥 Webhook | Repo: {repo_full_name} | Event: {event_type}")

    background_tasks.add_task(
        process_webhook_event, 
        payload.model_dump(), 
        event_type
    )
    
    return {
        "status": "success",
        "repository": repo_full_name,
        "event": event_type
    }


async def process_webhook_event(payload: dict, event_type: str):
    """Process and Save Event"""
    try:
        repo_service = RepositoryService()
        repo = repo_service.get_or_create_repository(payload.get("repository", {}))
        
        with next(get_session()) as session:
            change_event = ChangeEvent(
                repository_id=repo.id,
                commit_sha=payload.get("after", "unknown")[:40] if payload.get("after") else "unknown",
                pr_number=payload.get("number"),
                event_type=event_type,
                changes={
                    "repository": payload.get("repository", {}).get("full_name"),
                    "sender": payload.get("sender", {}).get("login"),
                    "event_summary": f"{event_type} event received"
                },
                processed=False
            )
            
            session.add(change_event)
            session.commit()
            detector = ChangeDetector()
            detector.analyze_change(change_event.id)
            
            print(f"✅ Event Saved | Repo ID: {repo.id} | Event ID: {change_event.id}")
            
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")