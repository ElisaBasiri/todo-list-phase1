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

                    elif sub_choice == "a":
                        # Add task
                        title = input("Task title (max 30 words): ").strip()
                        if not title:
                            print("→ Title cannot be empty")
                            continue

                        desc = input("Description (optional): ").strip()
                        deadline_str = get_valid_date("Deadline (YYYY-MM-DD or empty): ")

                        try:
                            task = manager.add_task(
                                project_id=proj_id,
                                title=title,
                                description=desc,
                                deadline_str=deadline_str or "",
                            )
                            print(f"→ Task '{task.title}' added (ID: {task.task_id})")
                        except ValueError as e:
                            print(f"Error: {e}")

                    elif sub_choice == "b":
                        # List tasks
                        tasks = manager.list_tasks(proj_id)
                        if not tasks:
                            print("→ No tasks in this project yet.")
                            continue

                        print(f"\nTasks in '{project.name}':")
                        for t in tasks:
                            dl = f" | Due: {t.deadline}" if t.deadline else ""
                            print(f"  {t.task_id:3d} | {t.title:<40} | {t.status.value.upper():<6}{dl}")

                    elif sub_choice == "c":
                        # Change status
                        task_id_str = input("Task ID: ").strip()
                        status_input = input("New status (todo / doing / done): ").strip().lower()

                        try:
                            manager.change_task_status(proj_id, int(task_id_str), status_input)
                            print("→ Task status updated successfully")
                        except ValueError as e:
                            print(f"Error: {e}")

                    elif sub_choice == "d":
                        # Edit task
                        task_id_str = input("Task ID: ").strip()
                        print("Leave blank for no change")
                        title = input("New title: ").strip() or None
                        desc = input("New description: ").strip() or None
                        status = input("New status (todo/doing/done): ").strip().lower() or None
                        dl = get_valid_date("New deadline (YYYY-MM-DD or empty to remove): ")

                        try:
                            manager.update_task(
                                proj_id, int(task_id_str),
                                title=title,
                                description=desc,
                                status_str=status,
                                deadline_str=dl,
                            )
                            print("→ Task updated successfully")
                        except ValueError as e:
                            print(f"Error: {e}")

                    elif sub_choice == "e":
                        # Delete task
                        task_id_str = input("Task ID to delete: ").strip()
                        try:
                            manager.delete_task(proj_id, int(task_id_str))
                            print("→ Task deleted successfully")
                        except ValueError as e:
                            print(f"Error: {e}")

                    else:
                        print("→ Invalid choice")

            except ValueError:
                print("→ Project ID must be a number")

        elif choice == "4":
            # Edit project
            proj_id_str = input("Project ID to edit: ").strip()
            try:
                proj_id = int(proj_id_str)
                name = input("New name (leave blank = no change): ").strip() or None
                desc = input("New description (leave blank = no change): ").strip() or None

                manager.update_project(proj_id, name, desc)
                print("→ Project updated successfully")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            # Delete project
            proj_id_str = input("Project ID to delete: ").strip()
            try:
                proj_id = int(proj_id_str)
                confirm = input(f"Delete project {proj_id} and all its tasks? (yes/no): ").strip().lower()
                if confirm in ("yes", "y"):
                    manager.delete_project(proj_id)
                    print("→ Project and all tasks deleted")
                    if current_project_id == proj_id:
                        current_project_id = None
                else:
                    print("→ Delete cancelled")
            except ValueError as e:
                print(f"Error: {e}")

        else:
            print("→ Invalid choice. Please enter 0-5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error:\n{e}")
        sys.exit(1)
