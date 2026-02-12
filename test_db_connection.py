from app.db.session import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("اتصال موفق به دیتابیس:", result.scalar())
except Exception as e:
    print("خطا در اتصال:", str(e))