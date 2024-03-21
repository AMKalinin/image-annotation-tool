from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.api import deps
from app import crud


router = APIRouter()

@router.get('')
def get_all_mask_in_task(*, db: Session = Depends(deps.get_db), project_name:str):
    return crud.classes.get_all(db, project_name)