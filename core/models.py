from datetime import date
from enum import Enum
from typing import List, Optional


class TaskStatus(Enum):
    """Allowed status values for a task"""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class Task:
    """Model representing a single task inside a project"""

    def __init__(
        self,
        title: str,
        description: str = "",
        status: TaskStatus = TaskStatus.TODO,
        deadline: Optional[date] = None,
        task_id: Optional[int] = None,
    ):
        
        if len(title.split()) > 30:
            raise ValueError("Task title must not exceed 30 words")
        if len(description.split()) > 150:
            raise ValueError("Task description must not exceed 150 words")
        
        self.task_id: Optional[int] = task_id
        self.title: str = title.strip()
        self.description: str = description.strip()
        self.status: TaskStatus = status
        self.deadline: Optional[date] = deadline



    def change_status(self, new_status: TaskStatus) -> None:
        """Change the status of the task"""
        self.status = new_status

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        deadline: Optional[date] = None,
    ) -> None:
        """Update one or more fields of the task"""
        if title is not None:
            if len(title.split()) > 30:
                raise ValueError("Task title must not exceed 30 words")
            self.title = title.strip()

        if description is not None:
            if len(description.split()) > 150:
                raise ValueError("Task description must not exceed 150 words")
            self.description = description.strip()

        if status is not None:
            self.status = status

        if deadline is not None:
            self.deadline = deadline


    def __str__(self) -> str:
        dl = f" (Due: {self.deadline})" if self.deadline else ""
        status_str = self.status.value.upper() if self.status else "UNKNOWN"
        return f"[{self.task_id or '-':3}] {self.title:<40} | {status_str:6} {dl}"
    

class Project:
    """Model representing a project that contains multiple tasks"""

    def __init__(
        self,
        name: str,
        description: str = "",
        project_id: Optional[int] = None,
    ):
        
        if len(name.split()) > 30:
            raise ValueError("Project name must not exceed 30 words")
        if len(description.split()) > 150:
            raise ValueError("Project description must not exceed 150 words")

        self.project_id: Optional[int] = project_id
        self.name: str = name.strip()
        self.description: str = description.strip()
        self.tasks: List[Task] = []
        self._next_task_id: int = 1


    def add_task(
        self,
        title: str,
        description: str = "",
        deadline: Optional[date] = None,
    ) -> Task:
        """Add a new task to the project"""
        task = Task(
            title=title,
            description=description,
            deadline=deadline,
            task_id=self._next_task_id,
        )
        self.tasks.append(task)
        self._next_task_id += 1
        return task
    

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def remove_task(self, task_id: int) -> bool:
        """Remove a task from the project's task list"""
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[i]
                return True
        return False