# app/models/project.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Project(Base):
    """SQLAlchemy model for Project table"""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(String(1024), nullable=False, default="")

    # One-to-Many relationship with Task
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",  # حذف پروژه → حذف تمام تسک‌هایش
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}')>" 
