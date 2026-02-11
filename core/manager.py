from typing import Dict, List, Optional
from .models import Project, Task, TaskStatus

class ToDoManager:
    """Main manager for projects and tasks - In-Memory storage"""

    def __init__(self):
        self.projects: Dict[int, Project] = {}  # project_id → Project
        self._next_project_id: int = 1

