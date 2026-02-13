# app/repositories/task_repository.py
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.task import Task, TaskStatus
from app.models.project import Project
from app.exceptions.repository_exceptions import RepositoryError, NotFoundError


class TaskRepository:
    """Repository for Task entity - handles all database operations for Tasks"""

    def __init__(self, db: Session):
        self.db = db

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str = "",
        status: TaskStatus = TaskStatus.TODO,
        deadline: Optional[date] = None,
    ) -> Task:
        """Create a new task inside a project"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError(f"Project with ID {project_id} not found")

        try:
            task = Task(
                title=title,
                description=description,
                status=status,
                deadline=deadline,
                project_id=project_id,
            )
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            return task
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"Failed to create task: {str(e)}")

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a single task by ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """Get all tasks of a specific project, sorted by ID"""
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id)
            .order_by(Task.id)
            .all()
        )

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        deadline: Optional[date] = None,
    ) -> Task:
        """Update task fields"""
        task = self.get_task_by_id(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")

        try:
            if title is not None:
                task.title = title.strip()

            if description is not None:
                task.description = description.strip()

            if status is not None:
                task.status = status

            if deadline is not None:  # None means remove deadline
                task.deadline = deadline

            self.db.commit()
            self.db.refresh(task)
            return task
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"Failed to update task: {str(e)}")

    def change_task_status(self, task_id: int, status: TaskStatus) -> Task:
        """Change only the status of a task"""
        return self.update_task(task_id, status=status)

    def delete_task(self, task_id: int) -> None:
        """Delete a task"""
        task = self.get_task_by_id(task_id)
        if not task:
            raise NotFoundError(f"Task with ID {task_id} not found")

        try:
            self.db.delete(task)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"Failed to delete task: {str(e)}")

    def count_tasks_in_project(self, project_id: int) -> int:
        """Count number of tasks in a project (useful for limits)"""
        return self.db.query(func.count(Task.id)).filter(Task.project_id == project_id).scalar()

    def get_overdue_tasks(self) -> List[Task]:
        """Get tasks that are overdue (deadline passed + not DONE)"""
        from datetime import date
        today = date.today()
        return (
            self.db.query(Task)
            .filter(Task.deadline < today)
            .filter(Task.status != TaskStatus.DONE)
            .all()
        ) 
