# app/commands/scheduler.py
"""
Background scheduler using 'schedule' library to periodically run
the auto-close overdue tasks command.
Run this in a separate terminal / process.
"""

import schedule
import time
from datetime import datetime

from app.db.session import SessionLocal
from app.commands.autoclose_overdue import autoclose_overdue_tasks


def job():
    """Wrapper that creates a fresh DB session for each scheduled run"""
    print(f"[{datetime.now()}] Scheduled check for overdue tasks started...")
    
    db = SessionLocal()
    try:
        closed_count = autoclose_overdue_tasks(db)
        print(f"[{datetime.now()}] Scheduled run finished. Closed {closed_count} tasks.")
    except Exception as e:
        print(f"[{datetime.now()}] Error during scheduled run: {str(e)}")
    finally:
        db.close()


def run_scheduler():
    # برای تست سریع می‌توانید این خط را به ۱ دقیقه تغییر دهید:
    #schedule.every(1).minutes.do(job)

    
    # تنظیم اصلی پروژه (هر ۱۵ دقیقه)
    schedule.every(15).minutes.do(job)
    
    print("Scheduler started. Checking for overdue tasks every 15 minutes.")
    print("Press Ctrl+C to stop the scheduler.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()