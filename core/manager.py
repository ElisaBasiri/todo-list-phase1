from typing import Dict, List, Optional
from .models import Project, Task, TaskStatus

class ToDoManager:
    """Main manager for projects and tasks - In-Memory storage"""

    def __init__(self):
        self.projects: Dict[int, Project] = {}  # project_id → Project
        self._next_project_id: int = 1

    # ───────────────────── Projects ─────────────────────

    def create_project(self, name: str, description: str = "") -> Project:
        if len(self.projects) >= MAX_PROJECTS:
            raise ValueError(f"Maximum number of projects ({MAX_PROJECTS}) has been reached")

        if any(p.name == name for p in self.projects.values()):
            raise ValueError("Project name already exists")

        project = Project(name=name, description=description, project_id=self._next_project_id)
        self.projects[self._next_project_id] = project
        self._next_project_id += 1
        return project