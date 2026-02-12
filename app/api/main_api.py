from fastapi import FastAPI
from app.api.routers.project_router import router as project_router
from app.api.routers.task_router import router as task_router

app = FastAPI(
    title="ToDoList API",
    description="Web API for ToDoList project",
    version="1.0.0"
)

app.include_router(project_router, prefix="/api", tags=["projects"])
app.include_router(task_router, prefix="/api", tags=["tasks"])