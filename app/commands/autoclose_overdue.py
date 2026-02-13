# app/commands/autoclose_overdue.py
"""
Command to automatically close overdue tasks.
This script can be run manually or scheduled via cron / schedule library.
"""

from datetime import date
from typing import List

from sqlalchemy.orm import Session

from app.db.session import SessionLocal  # یا get_db generator اگر از FastAPI استفاده می‌کنی
from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.repositories.project_repository import ProjectRepository


def autoclose_overdue_tasks(db: Session) -> int:
    """
    Find all overdue tasks (deadline < today and status != DONE)
    and set their status to DONE + set closed_at = today.

    Returns:
        int: number of tasks that were closed
    """
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    task_service = TaskService(task_repo=task_repo, project_repo=project_repo)

    # دریافت تسک‌های عقب‌افتاده
    overdue_tasks: List[Task] = task_service.get_overdue_tasks()

    if not overdue_tasks:
        print("No overdue tasks found.")
        return 0

    today = date.today()
    updated_count = 0

    for task in overdue_tasks:
        try:
            # تغییر وضعیت به DONE
            task_service.change_task_status(task.id, "done")

            # به‌روزرسانی closed_at
            # نکته: چون change_task_status فقط status را تغییر می‌دهد،
            # باید مستقیماً closed_at را هم آپدیت کنیم یا متد جدیدی اضافه کنیم
            task.closed_at = today

            db.add(task)  # برای اطمینان از track شدن تغییر
            updated_count += 1

            print(f"Task {task.id} ({task.title}) marked as DONE. Closed at: {today}")

        except Exception as e:
            print(f"Error closing task {task.id}: {str(e)}")
            db.rollback()
            continue

    if updated_count > 0:
        db.commit()
        print(f"Successfully closed {updated_count} overdue tasks.")
    else:
        db.rollback()

    return updated_count


def run_autoclose():
    """Entry point for running the command (manual or scheduled)"""
    db = SessionLocal()
    try:
        count = autoclose_overdue_tasks(db)
        return count
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting auto-close overdue tasks command...")
    closed_count = run_autoclose()
    print(f"Command finished. Closed {closed_count} tasks.") 
