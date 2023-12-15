from typing import Any
from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.schemas.task import TaskBase
from sqlalchemy.orm import Session
from app.api import deps
from app import crud


router = APIRouter()

@router.get('', response_model=list[TaskBase])
def get_all_tasks_in_project(*, db: Session=Depends(deps.get_db), project_name:str) -> Any:
    return crud.task.get_all(db, project_name)

@router.get('/{task_id}', response_model=TaskBase)
def get_task(*, db:Session=Depends(deps.get_db), project_name:str, task_id:int) -> Any:
    return crud.task.get_by_id(db, project_name, task_id)

@router.get('/{task_id}/icon')
def get_task_icon(project_name:str, task_id:int) -> Response:
    task_icon = crud.task.get_icon(project_name, task_id)
    return Response(content=task_icon, media_type="image/png")

@router.get('/{task_id}/layer/{layer_number}/tile/{x}:{y}')
def get_task_icon(project_name:str, 
                  task_id:int, 
                  layer_number:int, 
                  x:int, y:int) -> Response:
    task_tile = crud.task.get_tile(project_name, 
                                   task_id,
                                   layer_number, 
                                   x, y)
    return Response(content=task_tile, media_type="image/png")

@router.put('/{task_id}')
def update_task_status(project_name:str, task_id:int):
    ...