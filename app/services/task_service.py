# app/services/task_service.py
from typing import List, Optional
from datetime import date
from app.models.task import Task, TaskStatus
from app.models.project import Project
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.exceptions.service_exceptions import (
    ValidationError,
    NotFoundError,
    LimitExceededError
)
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Read all constraints from .env
MAX_TASKS_PER_PROJECT = int(os.getenv("MAX_NUMBER_OF_TASK", 50))
MAX_WORDS_TASK_TITLE   = int(os.getenv("MAX_WORDS_TASK_TITLE",   30))
MAX_WORDS_TASK_DESC    = int(os.getenv("MAX_WORDS_TASK_DESC",    150))


class TaskService:
    def __init__(
        self,
        task_repo: TaskRepository,
        project_repo: ProjectRepository,
    ):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def _validate_task_title(self, title: str) -> None:
        title = (title or "").strip()
        if not title:
            raise ValidationError("Task title cannot be empty")

        words_count = len(title.split())
        if words_count > MAX_WORDS_TASK_TITLE:
            raise ValidationError(
                f"Task title must not exceed {MAX_WORDS_TASK_TITLE} words"
            )

    def _validate_task_description(self, description: str) -> None:
        desc = (description or "").strip()
        words_count = len(desc.split())
        if words_count > MAX_WORDS_TASK_DESC:
            raise ValidationError(
                f"Task description must not exceed {MAX_WORDS_TASK_DESC} words"
            )

    def _parse_and_validate_deadline(self, deadline_str: Optional[str]) -> Optional[date]:
        if not deadline_str or not deadline_str.strip():
            return None
        try:
            return date.fromisoformat(deadline_str.strip())
        except ValueError:
            raise ValidationError("Invalid date format. Use: YYYY-MM-DD")

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str = "",
        status_str: str = "todo",
        deadline_str: Optional[str] = None,
    ) -> Task:
        project = self.project_repo.get_project_by_id(project_id)
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")

        task_count = self.task_repo.count_tasks_in_project(project_id)
        if task_count >= MAX_TASKS_PER_PROJECT:
            raise LimitExceededError(
                f"Maximum number of tasks in this project ({MAX_TASKS_PER_PROJECT}) has been reached"
            )

        self._validate_task_title(title)
        self._validate_task_description(description)

        deadline = self._parse_and_validate_deadline(deadline_str)

        try:
            status = TaskStatus[status_str.upper()]
        except (KeyError, ValueError):
            raise ValidationError("Invalid status. Allowed values: todo, doing, done")

        return self.task_repo.create_task(
            project_id=project_id,
            title=title.strip(),
            description=description.strip(),
            status=status,
            deadline=deadline,
        )

    def get_task(self, task_id: int) -> Task:
        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")
        return task

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status_str: Optional[str] = None,
        deadline_str: Optional[str] = None,
    ) -> Task:
        if title is not None:
            self._validate_task_title(title)

        if description is not None:
            self._validate_task_description(description)

        status = None
        if status_str is not None:
            try:
                status = TaskStatus[status_str.upper()]
            except (KeyError, ValueError):
                raise ValidationError("Invalid status. Allowed values: todo, doing, done")

        deadline = self._parse_and_validate_deadline(deadline_str)

        return self.task_repo.update_task(
            task_id=task_id,
            title=title.strip() if title is not None else None,
            description=description.strip() if description is not None else None,
            status=status,
            deadline=deadline,
        )

    def change_task_status(self, task_id: int, status_str: str) -> Task:
        try:
            status = TaskStatus[status_str.upper()]
        except (KeyError, ValueError):
            raise ValidationError("Invalid status. Allowed values: todo, doing, done")

        return self.task_repo.change_task_status(task_id, status)

    def delete_task(self, task_id: int) -> None:
        self.task_repo.delete_task(task_id)

    def list_tasks(self, project_id: int) -> List[Task]:
        project = self.project_repo.get_project_by_id(project_id)
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")
        return self.task_repo.get_tasks_by_project(project_id)

    def get_overdue_tasks(self) -> List[Task]:
        """Used for auto-closing overdue tasks job"""
        return self.task_repo.get_overdue_tasks()
    
    def close_task(self, task_id: int) -> Task:
        task = self.update_task(
            task_id=task_id,
            status_str="done"
        )
        task.closed_at = date.today()
        self.task_repo.db.commit()
        self.task_repo.db.refresh(task)
        return task