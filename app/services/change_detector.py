from sqlmodel import Session, select
from app.core.database import get_session
from app.domain.models.change_event import ChangeEvent
from datetime import datetime

class ChangeDetector:
    
    def analyze_change(self, change_event_id: int):
        """Analyze what changed in the code"""
        with next(get_session()) as session:
            event = session.get(ChangeEvent, change_event_id)
            if not event:
                return
            
            print(f"🔍 Analyzing changes for Event ID: {change_event_id}")
            
            # TODO: Later we will add git diff + Tree-sitter here
            # For now, basic classification
            changes = event.changes
            
            if "commits" in str(changes):
                change_type = "code_change"
            elif event.pr_number:
                change_type = "pull_request"
            else:
                change_type = "unknown"
            
            print(f"📊 Change Type Detected: {change_type}")
            
            # Mark as processed
            event.processed = True
            event.processed_at = datetime.utcnow()
            session.add(event)
            session.commit()
            
            print(f"✅ Change analysis completed for Event {change_event_id}")