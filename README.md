To Do List Project
(Phases 1 to 3 – In-Memory → RDB → Web API)
Final project for Software Engineering Course – Amirkabir University of Technology (AUT)
Prepared by: Elisa Basiri
Date: February 2026
Table of Contents

Introduction
Features
Prerequisites
Installation and Setup Step by Step
1. Clone the Project
2. Install Dependencies
3. Configure .env File
4. Start PostgreSQL Database
5. Apply Database Migrations (Alembic)
6. Run FastAPI Server (Web API) – Recommended Method
7. Run CLI (Command Line Interface) – Deprecated Method
8. Run Scheduler (Auto-Close Overdue Tasks)

Useful CLI Commands (Deprecated)
Testing the API with Swagger
Important Notes
Troubleshooting Common Issues
Project Structure

Introduction
This project was developed in three phases:

Phase 1 – In-Memory Storage with simple OOP (data stored only in RAM, lost on exit)
Phase 2 – Migration to Relational Database (PostgreSQL + SQLAlchemy + Alembic + Repository Pattern + Service Layer + Scheduler for auto-closing overdue tasks)
Phase 3 – Conversion to Web API with FastAPI (RESTful endpoints + Pydantic validation + Swagger docs + Synchronous/Asynchronous endpoints)

Important: The CLI interface (from Phases 1 and 2) has been deprecated in Phase 3 and is maintained only for temporary compatibility. We strongly recommend using the API. A deprecation warning is displayed when running the CLI.
This is a To Do List management system that handles projects and tasks, with Phase 1 constraints (max 10 projects, 50 tasks per project, word limits) and auto-closing overdue tasks.
Features

Persistent data storage in PostgreSQL with One-to-Many relationships
Project and task management using Repository Pattern and Service Layer
Phase 1 constraints (max projects, max tasks, word limits) fully enforced
Auto-closing overdue tasks with a scheduler (every 15 minutes)
Deprecated CLI with deprecation warning
Full Web API with FastAPI (CRUD for projects and tasks, with Pydantic validation)
Automatic documentation with Swagger UI and Redoc
Strong input/output validation
API versioning (e.g., /api/v1/)
Uniform response structure (status, data, message)

Prerequisites

Python 3.10 or higher
Poetry (for dependency management)
Docker + Docker Compose (for PostgreSQL)
Git

Installation and Setup Step by Step
1. Clone the Project

Bashgit clone https://github.com/ElisaBasiri/todo-list-phase1.git
/cd todo-list-phase1/
2. Install Dependencies
/poetry install/
This installs all dependencies (including FastAPI, Uvicorn, Pydantic, SQLAlchemy, Alembic, APScheduler, etc.).
3. Configure .env File
Copy the example file and edit the values:
/cp .env.example .env/
Suggested .env content:
env# Database (change password!)
DATABASE_URL=postgresql://todolist_user:your_secure_password@localhost:5433/todolist_db

# Phase 1 & 2 limits
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=50
MAX_TASK_WORDS=100

# Optional: show SQL queries
SQLALCHEMY_ECHO=false

# API Settings (optional)
API_VERSION=v1
Warning: Change the database password immediately.
4. Start PostgreSQL Database
/docker compose up -d/
Check if the container is running:
Bashdocker compose ps
The database is mapped to port 5433 to avoid conflicts with local PostgreSQL.
5. Apply Database Migrations (Alembic)
/poetry run alembic upgrade head/
If it fails, ensure the database is running and DATABASE_URL is correct.
6. Run FastAPI Server (Web API) – Recommended Method
/poetry run python main.py api/

Server address: http://127.0.0.1:8000/api/v1/
Swagger docs: http://127.0.0.1:8000/docs
Redoc docs: http://127.0.0.1:8000/redoc

This supports async endpoints for better performance.
7. Run CLI (Command Line Interface) – Deprecated Method
Important Warning: The CLI is deprecated in Phase 3 and will be removed in future releases. Use the Web API instead. A deprecation warning will be displayed on startup.
poetry run python main.py
After running, you will see:
textWARNING: CLI interface is deprecated and will be removed in the next release. Please use the FastAPI HTTP interface instead.
Then the text menu from previous phases will appear.
8. Run Scheduler (Auto-Close Overdue Tasks)
Run in a separate terminal:
poetry run python -m app.commands.scheduler
This process checks and closes overdue tasks every 15 minutes. For quick testing, change the interval in app/commands/scheduler.py to every(30).seconds.do(job).
Useful CLI Commands (Deprecated)
After running poetry run python main.py and seeing the deprecation warning, the menu appears:

1 → Create new project
2 → List all projects
3 → Select project and manage tasks (add, list, change status, edit, delete task)
4 → Edit project
5 → Delete project
0 → Exit

Recommendation: Switch to API endpoints instead of CLI.
Testing the API with Swagger

Start the FastAPI server (Step 6).
Go to http://127.0.0.1:8000/docs.
Test all endpoints (e.g., /api/v1/projects, /api/v1/projects/{id}/tasks) directly.
Enter inputs and click "Execute" to see responses.

Sample endpoints:

GET /api/v1/projects → List projects
POST /api/v1/projects → Create project
GET /api/v1/projects/{project_id} → Get project details
DELETE /api/v1/projects/{project_id} → Delete project
GET /api/v1/projects/{project_id}/tasks → List tasks
POST /api/v1/projects/{project_id}/tasks → Create task

Important Notes

The database is mapped to port 5433 to avoid conflicts with local PostgreSQL.
If port 5433 is occupied, change it in docker-compose.yml and update DATABASE_URL.
For resetting the database and starting fresh:Bashdocker compose down -v
docker compose up -d
poetry run alembic upgrade head
Security: In production, use HTTPS (this README uses HTTP for local development).
The scheduler should run continuously (or scheduled via cron on Linux or Task Scheduler on Windows).

Troubleshooting Common Issues

Database connection error: Check if Docker is running, DATABASE_URL is correct, and port 5433 is free.
Alembic error: Re-run alembic upgrade head or check revisions.
ModuleNotFoundError: Re-run poetry install.
CLI not running: Check main.py and ensure deprecation is implemented.
FastAPI error: Verify dependencies (fastapi, uvicorn installed).
Scheduler not working: Ensure overdue tasks exist and interval is correct.

Project Structure (Summary)
texttodo-list-phase1/
├── app/
│   ├── api/                # Routers and FastAPI endpoints
│   ├── cli/                # Deprecated CLI
│   ├── commands/           # Scheduler and auto-close
│   ├── db/                 # SQLAlchemy models, session, base
│   ├── exceptions/         # Custom exceptions
│   ├── repositories/       # Repository Pattern
│   ├── services/           # Business logic + validation
│   ├── schemas/            # Pydantic models for validation
│   └── main.py             # CLI entry point (deprecated)
├── alembic/                # Migration files
├── alembic.ini             # Alembic config
├── docker-compose.yml      # Docker for Postgres
├── .env                    # Environment variables
├── .env.example
├── main_api.py             # FastAPI app entry
├── pyproject.toml          # Poetry config
└── README.md
This structure follows Layered Architecture: API → Service → Repository → DB.
The project is ready! If you have questions or need changes, raise an issue on the repo.

