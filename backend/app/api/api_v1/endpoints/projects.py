from typing import Any, Annotated, List
from fastapi import APIRouter, Depends, UploadFile, Form

from app.schemas.project import ProjectOut, ProjectIn
from app.schemas.classes import ClassesLst
from sqlalchemy.orm import Session
from app.api import deps
from app import crud

router = APIRouter()

@router.get('', response_model=list[ProjectOut])
def get_all_projects(db: Session = Depends(deps.get_db)) -> Any:
    return crud.project.get_all(db)

@router.post('/create', response_model=ProjectOut)
def create_project(*, db: Session = Depends(deps.get_db),
                    files: List[UploadFile],
                    project_name: Annotated[str, Form()],
                    creator: Annotated[str, Form()],
                    description: Annotated[str, Form()],
                    classes: Annotated[ClassesLst, Form()]) -> Any:   # Может быть будет работать и без этого, надо проверить потом
    project = crud.project.create(db, ProjectIn(name=project_name,
                                                  creator=creator,
                                                  description=description))
    crud.task.create_tasks(db, project_name, files)
    crud.classes.create_classes(db, project_name, classes.classes_list)
    return project

@router.post('/create-based', response_model=ProjectOut)
def create_project_bases(*, db: Session = Depends(deps.get_db), project_in: ProjectOut) -> Any: #ref projectIn
    ...

@router.get('/{project_name}', response_model=ProjectOut)
def get_project(*, db: Session = Depends(deps.get_db), project_name:str) -> Any:
    project = crud.project.get_by_name(db, project_name)
    return project

@router.delete('/{project_name}')
def delete_project(*, db: Session = Depends(deps.get_db), project_name:str) -> Any:
    crud.project.delete_by_name(db, project_name)
