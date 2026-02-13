from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.task_service import TaskService  
from app.api.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.repositories.task_repository import TaskRepository  
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

def get_task_service(db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    return TaskService(repository)

@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(project_id: int, task: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.create_task(project_id, task.title, task.description, task.due_date, task.status)

@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(project_id: int, service: TaskService = Depends(get_task_service)):
    return service.get_tasks_by_project(project_id)

@router.get("/projects/{project_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(project_id: int, task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task(task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/projects/{project_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(project_id: int, task_id: int, task: TaskUpdate, service: TaskService = Depends(get_task_service)):
    updated = service.update_task(task_id, task.title, task.description, task.due_date, task.status)
    if not updated or updated.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/projects/{project_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(project_id: int, task_id: int, service: TaskService = Depends(get_task_service)):
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")