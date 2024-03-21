from fastapi import APIRouter

from app.api.api_v1.endpoints import projects
from app.api.api_v1.endpoints import tasks
from app.api.api_v1.endpoints import masks
from app.api.api_v1.endpoints import classes

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(tasks.router, prefix="/projects/{project_name}/tasks", tags=["tasks"])
api_router.include_router(masks.router, prefix="/projects/{project_name}/tasks/{task_id}/masks", tags=["masks"])
api_router.include_router(classes.router, prefix="/projects/{project_name}/classes", tags=["classes"])