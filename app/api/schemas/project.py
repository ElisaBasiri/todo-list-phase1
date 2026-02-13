from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.api.schemas.task import TaskResponse  # Forward ref if needed

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the project")
    description: Optional[str] = Field(None, max_length=500, description="Project description")

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    tasks: List[TaskResponse] = []  # If you want to include tasks

    class Config:
        from_attributes = True  # For SQLAlchemy ORM