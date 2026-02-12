# app/services/project_service.py
from typing import List, Optional
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.exceptions.service_exceptions import (
    ValidationError,
    NotFoundError,
    DuplicateError,
    LimitExceededError
)
import os
from dotenv import load_dotenv

load_dotenv()

MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECT", 10))
MAX_WORDS_PROJECT_NAME = 30
MAX_WORDS_PROJECT_DESC = 150


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    def _validate_project_name(self, name: str, exclude_id: Optional[int] = None) -> None:
        """نام پروژه نباید تکراری باشد و محدودیت طول کلمه داشته باشد"""
        if not name.strip():
            raise ValidationError("Project name cannot be empty")

        words = name.strip().split()
        if len(words) > MAX_WORDS_PROJECT_NAME:
            raise ValidationError(f"Project name must not exceed {MAX_WORDS_PROJECT_NAME} words")

        existing = self.project_repo.get_project_by_name(name.strip())
        if existing and existing.id != exclude_id:
            raise DuplicateError(f"Project name '{name}' already exists")

    def _validate_project_description(self, description: str) -> None:
        words = description.strip().split()
        if len(words) > MAX_WORDS_PROJECT_DESC:
            raise ValidationError(f"Project description must not exceed {MAX_WORDS_PROJECT_DESC} words")

    def create_project(self, name: str, description: str = "") -> Project:
        # اعتبارسنجی‌های فاز ۱
        self._validate_project_name(name)
        self._validate_project_description(description)

        # چک محدودیت تعداد پروژه‌ها
        if self.project_repo.count_projects() >= MAX_PROJECTS:
            raise LimitExceededError(f"Maximum number of projects ({MAX_PROJECTS}) has been reached")

        return self.project_repo.create_project(name.strip(), description.strip())

    def get_project(self, project_id: int) -> Project:
        project = self.project_repo.get_project_by_id(project_id)
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")
        return project

    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        if name is not None:
            self._validate_project_name(name, exclude_id=project_id)

        if description is not None:
            self._validate_project_description(description)

        return self.project_repo.update_project(
            project_id=project_id,
            name=name.strip() if name else None,
            description=description.strip() if description else None
        )

    def delete_project(self, project_id: int) -> None:
        self.project_repo.delete_project(project_id)

    def list_projects(self) -> List[Project]:
        return self.project_repo.list_projects()

    def get_project_by_name(self, name: str) -> Optional[Project]:
        return self.project_repo.get_project_by_name(name) 
