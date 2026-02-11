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