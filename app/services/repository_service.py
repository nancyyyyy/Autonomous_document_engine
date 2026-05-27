from sqlmodel import Session, select
from app.domain.models.repository import Repository
from app.core.database import get_session

class RepositoryService:
    
    def get_or_create_repository(self, github_repo_data: dict):
        """Get or create repository from GitHub payload"""
        with next(get_session()) as session:
            
            full_name = github_repo_data.get("full_name")
            
            # Check if repo already exists
            statement = select(Repository).where(Repository.full_name == full_name)
            repo = session.exec(statement).first()
            
            if repo:
                return repo
            
            # Create new repository
            new_repo = Repository(
                github_id=github_repo_data.get("id"),
                owner=github_repo_data.get("owner", {}).get("login", "unknown"),
                name=github_repo_data.get("name"),
                full_name=full_name,
                default_branch=github_repo_data.get("default_branch", "main")
            )
            
            session.add(new_repo)
            session.commit()
            session.refresh(new_repo)
            
            print(f"✅ New Repository registered: {full_name}")
            return new_repo