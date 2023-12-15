from typing import Any
from fastapi import APIRouter, Depends

from app.schemas.mask import MaskBase
from sqlalchemy.orm import Session
from app.api import deps
from app import crud


router = APIRouter()

@router.get('')
def get_all_mask_in_task(*, db: Session = Depends(deps.get_db), project_name:str, task_id:int):
    return crud.mask.get_all(db, project_name, task_id)

@router.post('/create', response_model=MaskBase)
def create_mask(*, db: Session = Depends(deps.get_db), project_name:str, task_id:int, mask_in: MaskBase) -> Any:
    mask = crud.mask.create(db, mask_in)
    return mask

@router.put('/{mask_id}')
def update_mask(project_name:str, task_id:int, mask_id:int) -> Any:
    #TODO
    ...

@router.delete('/{mask_id}')
def delete_mask(project_name:str, task_id:int, mask_id:int) -> Any:
    #TODO
    ...
    