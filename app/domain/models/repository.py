from sqlmodel import Field
from typing import Optional
from datetime import datetime
from app.domain.models.base import BaseModel

class Repository(BaseModel, table=True):
    __tablename__ = "repositories"
    
    github_id: int = Field(unique=True, index=True)
    owner: str = Field(max_length=100)
    name: str = Field(max_length=100)
    full_name: str = Field(unique=True, max_length=200)
    default_branch: str = "main"
    last_synced: Optional[datetime] = None
    is_active: bool = True
