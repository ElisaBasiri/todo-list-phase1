# create_test_overdue.py
from datetime import date, timedelta
from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

db = SessionLocal()
try:
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    task_service = TaskService(task_repo, project_repo)

    # ساخت پروژه تست (اگر قبلاً ساختی، می‌توانی از ID موجود استفاده کنی)
    project = project_repo.create_project(name="Test Overdue Project", description="For testing auto-close")
    print(f"Project created: ID={project.id}")

    # ساخت تسک با deadline در گذشته (مثلاً ۱۰ روز قبل)
    overdue_date = date.today() - timedelta(days=10)

    task = task_service.create_task(
        project_id=project.id,
        title="Overdue Test Task",
        description="This should be auto-closed",
        status_str="todo",
        deadline_str=overdue_date.isoformat()
    )
    print(f"Overdue task created: ID={task.id}, deadline={task.deadline}")

except Exception as e:
    print("Error:", str(e))
finally:
    db.close()