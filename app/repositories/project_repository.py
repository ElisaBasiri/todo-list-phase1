# app/repositories/project_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.project import Project
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError, DuplicateError


class ProjectRepository:
    """Repository for Project entity - handles all database operations for Projects"""

    def __init__(self, db: Session):
        self.db = db

    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project"""
        try:
            project = Project(name=name, description=description)
            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)
            return project
        except IntegrityError:
            self.db.rollback()
            raise DuplicateError(f"Project name '{name}' already exists")
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"Failed to create project: {str(e)}")

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Get a project by its ID (with tasks eager loaded if needed)"""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get a project by its unique name"""
        return self.db.query(Project).filter(Project.name == name).first()

    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        """Update project fields"""
        project = self.get_project_by_id(project_id)
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")

        try:
            if name is not None:
                project.name = name.strip()

            if description is not None:
                project.description = description.strip()

            self.db.commit()
            self.db.refresh(project)
            return project
        except IntegrityError:
            self.db.rollback()
            raise DuplicateError(f"Project name '{name}' already exists")
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"Failed to update project: {str(e)}")

    def delete_project(self, project_id: int) -> None:
        """Delete project (cascades to tasks due to ON DELETE CASCADE)"""
        project = self.get_project_by_id(project_id)
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")

        try:
            self.db.delete(project)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"Failed to delete project: {str(e)}")

    def list_projects(self) -> List[Project]:
        """Return all projects sorted by ID"""
        return self.db.query(Project).order_by(Project.id).all()

    def count_projects(self) -> int:
        """Return total number of projects (useful for limits)"""
        return self.db.query(Project).count() 
