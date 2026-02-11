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
    
    def get_project(self, project_id: int) -> Optional[Project]:
        return self.projects.get(project_id)

    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        if name is not None:
            if any(p.name == name and p.project_id != project_id for p in self.projects.values()):
                raise ValueError("Project name already exists")
            if len(name.split()) > 30:
                raise ValueError("Project name must not exceed 30 words")
            project.name = name.strip()

        if description is not None:
            if len(description.split()) > 150:
                raise ValueError("Project description must not exceed 150 words")
            project.description = description.strip()

    def delete_project(self, project_id: int) -> None:
        """Delete project + Cascade Delete (all associated tasks are also removed)"""
        if project_id not in self.projects:
            raise ValueError(f"Project with ID {project_id} not found")
        del self.projects[project_id]

    def list_projects(self) -> List[Project]:
        """Return list of projects sorted by ID"""
        return sorted(self.projects.values(), key=lambda p: p.project_id or 0)
    
    def add_task(
        self,
        project_id: int,
        title: str,
        description: str = "",
        deadline_str: str = "",
    ) -> Task:
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        if len(project.tasks) >= MAX_TASKS_PER_PROJECT:
            raise ValueError(f"Maximum number of tasks in project ({MAX_TASKS_PER_PROJECT}) has been reached")

        deadline = None
        if deadline_str.strip():
            try:
                deadline = date.fromisoformat(deadline_str.strip())
            except ValueError:
                raise ValueError("Invalid date format. Use: YYYY-MM-DD")

        return project.add_task(title=title, description=description, deadline=deadline)
    
    def change_task_status(
        self, project_id: int, task_id: int, status_str: str
    ) -> None:
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        task = project.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found in project")

        try:
            new_status = TaskStatus[status_str.upper()]
        except (KeyError, ValueError):
            raise ValueError("Invalid status. Allowed values: todo, doing, done")

        task.change_status(new_status)

