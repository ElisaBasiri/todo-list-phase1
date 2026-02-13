from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.project_service import ProjectService
from app.api.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.repositories.project_repository import ProjectRepository
from app.db.session import get_db  
from sqlalchemy.orm import Session

router = APIRouter()

def get_project_service(db: Session = Depends(get_db)):
    repository = ProjectRepository(db)
    return ProjectService(repository)

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, service: ProjectService = Depends(get_project_service)):
    return service.create_project(project.name, project.description)

@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(service: ProjectService = Depends(get_project_service)):
    return service.get_all_projects()

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectUpdate, service: ProjectService = Depends(get_project_service)):
    updated = service.update_project(project_id, project.name, project.description)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    deleted = service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")