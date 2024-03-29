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

@router.post('/create')
def create_mask(*, db: Session = Depends(deps.get_db), mask_in: MaskBase):
    mask = crud.mask.create(db, mask_in)
    return mask

@router.put('/{mask_id}')
def update_mask(project_name:str, task_id:int, mask_id:int) -> Any:
    #TODO
    ...

@router.delete('/{mask_id}')
def delete_mask(*, db: Session = Depends(deps.get_db), project_name:str, task_id:int, mask_id:int) -> Any:
    crud.mask.delete_by_id(db, project_name, task_id, mask_id)
    