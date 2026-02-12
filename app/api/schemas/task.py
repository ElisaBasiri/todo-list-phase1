from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[datetime] = None
    status: str = Field("pending", description="Task status: pending, in_progress, completed")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[datetime] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True