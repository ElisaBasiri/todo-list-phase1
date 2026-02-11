import sys
from datetime import date
from core.manager import ToDoManager
from core.models import TaskStatus


def print_header():
    print("\n" + "=" * 60)
    print("          ToDo List - Phase 1 (In-Memory)")
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





def main():
    manager = ToDoManager()
    current_project_id = None

    while True:
        print_header()
        print_main_menu()

        choice = input("Your choice (0-5): ").strip()

        if choice == "0":
            print("\nGoodbye! (Data is in-memory only – will be lost on exit)")
            sys.exit(0)

        elif choice == "1":
            # Create project
            name = input("Project name (max 30 words): ").strip()
            if not name:
                print("→ Project name cannot be empty")
                continue

            desc = input("Description (optional, max 150 words): ").strip()

            try:
                project = manager.create_project(name, desc)
                print(f"→ Project '{project.name}' created successfully (ID: {project.project_id})")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            # List projects
            projects = manager.list_projects()
            if not projects:
                print("→ No projects created yet.")
                continue

            print("\nProjects:")
            for p in projects:
                print(f"  {p.project_id:3d} | {p.name:<35} | {len(p.tasks)} tasks | {p.description[:50]}{'...' if len(p.description) > 50 else ''}")

        elif choice == "3":
            # Select project → enter task submenu
            proj_id_str = input("Enter project ID: ").strip()
            try:
                proj_id = int(proj_id_str)
                project = manager.get_project(proj_id)
                if not project:
                    print(f"→ Project ID {proj_id} not found")
                    continue

                current_project_id = proj_id
                print(f"→ Entered project '{project.name}' (ID: {proj_id})")

                # Task submenu loop
                while True:
                    print_task_menu(project.name)
                    sub_choice = input("Your choice: ").strip().lower()

                    if sub_choice == "q":
                        current_project_id = None
                        print("→ Back to main menu")
                        break