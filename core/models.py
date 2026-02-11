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