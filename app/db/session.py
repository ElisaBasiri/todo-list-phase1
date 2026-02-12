from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=getenv("SQLALCHEMY_ECHO", "false").lower() == "true")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
