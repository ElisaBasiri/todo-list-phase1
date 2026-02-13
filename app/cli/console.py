"""
    Deprecated: This CLI is deprecated. Use the FastAPI API instead.
"""



import sys
from datetime import date

from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.exceptions.service_exceptions import (
    ValidationError,
    NotFoundError,
    DuplicateError,
    LimitExceededError
)


import warnings

# At the top of the file or before main logic
warnings.warn(
    "WARNING: CLI interface is deprecated and will be removed in the next release. Please use the FastAPI HTTP interface instead.",
    DeprecationWarning,
    stacklevel=2
)

# Or print it
print("WARNING: CLI interface is deprecated. Use API endpoints instead.")

def print_header():
    print("\n" + "=" * 60)
    print("          ToDo List - Phase 2 (Relational Database)")
    print("     Software Engineering Course - AUT")
    print("=" * 60)


def print_main_menu():
    print("\nMain Menu:")
    print("  1. Create new project")
    print("  2. List all projects")
    print("  3. Select project and manage tasks")
    print("  4. Edit project")
    print("  5. Delete project")
    print("  0. Exit")
    print("-" * 60)


def print_task_menu(project_name: str):
    print(f"\nCurrent Project: {project_name}")
    print("Task Menu:")
    print("  a. Add new task")
    print("  b. List tasks in project")
    print("  c. Change task status")
    print("  d. Edit task")
    print("  e. Delete task")
    print("  q. Back to main menu")
    print("-" * 60)


def get_valid_date(prompt: str) -> str:
    while True:
        dl_str = input(prompt).strip()
        if not dl_str:
            return ""
        try:
            date.fromisoformat(dl_str)
            return dl_str
        except ValueError:
            print("→ Invalid date format. Use YYYY-MM-DD or leave empty.")


def main():
    db = SessionLocal()
    project_service = ProjectService(ProjectRepository(db))
    task_service = TaskService(TaskRepository(db), ProjectRepository(db))

    current_project_id = None

    try:
        while True:
            print_header()
            print_main_menu()

            choice = input("Your choice (0-5): ").strip()

            if choice == "0":
                print("\nGoodbye! Data is now stored in PostgreSQL.")
                break

            elif choice == "1":
                name = input("Project name (max 30 words): ").strip()
                if not name:
                    print("→ Project name cannot be empty")
                    continue

                desc = input("Description (optional, max 150 words): ").strip()

                try:
                    project = project_service.create_project(name, desc)
                    print(f"→ Project '{project.name}' created successfully (ID: {project.id})")
                except (ValidationError, DuplicateError, LimitExceededError) as e:
                    print(f"Error: {e}")

            elif choice == "2":
                projects = project_service.list_projects()
                if not projects:
                    print("→ No projects created yet.")
                    continue

                print("\nProjects:")
                for p in projects:
                    print(f"  {p.id:3d} | {p.name:<35} | {len(p.tasks)} tasks | {p.description[:50]}{'...' if len(p.description) > 50 else ''}")

            elif choice == "3":
                proj_id_str = input("Enter project ID: ").strip()
                try:
                    proj_id = int(proj_id_str)
                    project = project_service.get_project(proj_id)
                    if not project:
                        print(f"→ Project with ID {proj_id} not found")
                        continue

                    current_project_id = proj_id
                    print(f"→ Entered project '{project.name}' (ID: {proj_id})")

                    while True:
                        print_task_menu(project.name)
                        sub_choice = input("Your choice: ").strip().lower()

                        if sub_choice == "q":
                            current_project_id = None
                            print("→ Back to main menu")
                            break

                        elif sub_choice == "a":
                            title = input("Task title (max 30 words): ").strip()
                            if not title:
                                print("→ Title cannot be empty")
                                continue

                            desc = input("Description (optional): ").strip()
                            deadline_str = get_valid_date("Deadline (YYYY-MM-DD or empty): ")
                            status = input("Status (todo/doing/done) [default: todo]: ").strip().lower() or "todo"

                            try:
                                task = task_service.create_task(
                                    project_id=proj_id,
                                    title=title,
                                    description=desc,
                                    status_str=status,
                                    deadline_str=deadline_str
                                )
                                print(f"→ Task '{task.title}' added (ID: {task.id})")
                            except (NotFoundError, ValidationError, LimitExceededError) as e:
                                print(f"Error: {e}")

                        elif sub_choice == "b":
                            tasks = task_service.list_tasks(proj_id)
                            if not tasks:
                                print("→ No tasks in this project yet.")
                                continue

                            print(f"\nTasks in '{project.name}':")
                            for t in tasks:
                                dl = f" | Due: {t.deadline}" if t.deadline else ""
                                print(f"  {t.id:3d} | {t.title:<40} | {t.status.value.upper():<6}{dl}")

                        elif sub_choice == "c":
                            task_id_str = input("Task ID: ").strip()
                            status_input = input("New status (todo / doing / done): ").strip().lower()

                            try:
                                task_service.change_task_status(int(task_id_str), status_input)
                                print("→ Task status updated successfully")
                            except (NotFoundError, ValidationError) as e:
                                print(f"Error: {e}")

                        elif sub_choice == "d":
                            task_id_str = input("Task ID: ").strip()
                            print("Leave blank for no change")
                            title = input("New title: ").strip() or None
                            desc = input("New description: ").strip() or None
                            status = input("New status (todo/doing/done): ").strip().lower() or None
                            dl = get_valid_date("New deadline (YYYY-MM-DD or empty to remove): ")

                            try:
                                task_service.update_task(
                                    int(task_id_str),
                                    title=title,
                                    description=desc,
                                    status_str=status,
                                    deadline_str=dl
                                )
                                print("→ Task updated successfully")
                            except (NotFoundError, ValidationError) as e:
                                print(f"Error: {e}")

                        elif sub_choice == "e":
                            task_id_str = input("Task ID to delete: ").strip()
                            try:
                                task_service.delete_task(int(task_id_str))
                                print("→ Task deleted successfully")
                            except NotFoundError as e:
                                print(f"Error: {e}")

                        else:
                            print("→ Invalid choice")

                except ValueError:
                    print("→ Project ID must be a number")

            elif choice == "4":
                proj_id_str = input("Project ID to edit: ").strip()
                try:
                    proj_id = int(proj_id_str)
                    name = input("New name (leave blank = no change): ").strip() or None
                    desc = input("New description (leave blank = no change): ").strip() or None

                    project_service.update_project(proj_id, name, desc)
                    print("→ Project updated successfully")
                except (NotFoundError, ValidationError, DuplicateError) as e:
                    print(f"Error: {e}")

            elif choice == "5":
                proj_id_str = input("Project ID to delete: ").strip()
                try:
                    proj_id = int(proj_id_str)
                    confirm = input(f"Delete project {proj_id} and all its tasks? (yes/no): ").strip().lower()
                    if confirm in ("yes", "y"):
                        project_service.delete_project(proj_id)
                        print("→ Project and all tasks deleted")
                        if current_project_id == proj_id:
                            current_project_id = None
                    else:
                        print("→ Delete cancelled")
                except (NotFoundError, ValueError) as e:
                    print(f"Error: {e}")

            else:
                print("→ Invalid choice. Please enter 0-5.")

    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        print(f"\nUnexpected error:\n{e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()