from sqlmodel import Field, Column
from sqlalchemy import JSON as SA_JSON
from typing import Optional, Any, Dict
from datetime import datetime
from app.domain.models.base import BaseModel

class ChangeEvent(BaseModel, table=True):
    __tablename__ = "change_events"
    
    repository_id: int = Field(foreign_key="repositories.id")
    commit_sha: str = Field(max_length=40)
    pr_number: Optional[int] = None
    event_type: str = Field(max_length=20)        # "push", "pull_request"
    changes: Dict[str, Any] = Field(sa_column=Column(SA_JSON))   # Fixed
    processed: bool = False
    processed_at: Optional[datetime] = None