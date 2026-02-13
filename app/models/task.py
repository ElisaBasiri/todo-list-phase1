 # app/models/task.py
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class TaskStatus(str, PyEnum):
    """Task status enum (compatible with SQLAlchemy Enum)"""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class Task(Base):
    """SQLAlchemy model for Task table"""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String(1024), nullable=False, default="")
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    deadline = Column(Date, nullable=True)
    closed_at = Column(Date, nullable=True)  # جدید - برای overdue auto-close

    # Foreign key to Project
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    # Back-reference to Project
    project = relationship("Project", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status={self.status})>"
