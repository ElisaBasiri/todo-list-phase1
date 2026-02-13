# To Do List Project  
(Phases 1 to 3 – In-Memory → RDB → Web API)

Final project for Software Engineering Course – Amirkabir University of Technology (AUT)  
Prepared by: Elisa Basiri  
February 2026

This project was developed in three phases:

Phase 1: In-memory storage using simple OOP – data is lost when the program exits  
Phase 2: Migration to PostgreSQL + SQLAlchemy + Alembic + Repository & Service patterns + background scheduler for auto-closing overdue tasks  
Phase 3: Conversion to a modern Web API using FastAPI (the current recommended method)

The command-line interface (CLI) from earlier phases is **deprecated** starting from Phase 3 and is only kept for temporary backward compatibility.  
A deprecation warning is shown when running the CLI.  
**Strong recommendation:** Use the web API instead.

Constraints enforced (from Phase 1):
- Maximum 10 projects
- Maximum 50 tasks per project
- Maximum 100 words per task description
- Automatic closure of overdue tasks (checked every 15 minutes)

Main features:
- Persistent storage in PostgreSQL with one-to-many relationship (Project → Tasks)
- Layered architecture: Repository + Service
- Strict enforcement of Phase 1 constraints
- Background scheduler for closing overdue tasks
- Full REST API built with FastAPI + Pydantic + versioning /api/v1/
- Automatic interactive documentation (Swagger + ReDoc)
- Legacy CLI interface (with deprecation warning)

Prerequisites:
- Python 3.10 or newer
- Poetry
- Docker + Docker Compose
- Git

Installation & Setup (step by step):

1. git clone https://github.com/ElisaBasiri/todo-list-phase1.git
   cd todo-list-phase1

2. poetry install

3. cp .env.example .env
   Open the .env file and **change the password**:
   DATABASE_URL=postgresql://todolist_user:your_secure_password@localhost:5433/todolist_db
   MAX_NUMBER_OF_PROJECT=10
   MAX_NUMBER_OF_TASK=50
   MAX_TASK_WORDS=100
   SQLALCHEMY_ECHO=false

4. docker compose up -d

5. poetry run alembic upgrade head

6. Run the FastAPI server (recommended way):
   poetry run python main.py api
   → Open: http://127.0.0.1:8000/docs

Run the background scheduler (in a separate terminal):
poetry run python -m app.commands.scheduler

Run the old CLI (deprecated):
poetry run python main.py
→ Deprecation warning will appear

Important notes:
- The database runs on port **5433** to avoid conflict with any local PostgreSQL instance
- If port 5433 is occupied, change it in docker-compose.yml and update DATABASE_URL accordingly
- The scheduler must stay running; otherwise overdue tasks won't be closed automatically
- The CLI will be removed in future versions

Quick troubleshooting:
Cannot connect to database → Check `docker compose ps` / correct password in .env? / port 5433 free?
Alembic fails → Run `poetry run alembic upgrade head` again
Module not found → Run `poetry install` again
Scheduler does nothing → Do you have overdue tasks? Check interval in scheduler.py

Project structure (summary):
app/api           → FastAPI routes & endpoints
app/cli           → Deprecated command-line interface
app/commands      → Scheduler for closing overdue tasks
app/db            → SQLAlchemy models & connection
app/repositories  → Data access layer
app/services      → Business logic & validation
app/schemas       → Pydantic models
main.py           → CLI entry point (deprecated)
main_api.py       → FastAPI application
alembic/          → Database migrations
docker-compose.yml
.env
.env.example

The project is ready to use.  
Any questions or issues → please open an Issue.

Good luck!
