from sqlalchemy.orm import Session
from random import randint

from app.models.mask import Mask
from app.schemas.mask import MaskBase
from app.models.classes import Classes  #it is necessary for the relationship

class CRUDMask():
    def get_all(self, db:Session, project_name:str, task_id:int) -> list[Mask]:
        return db.query(Mask).filter(Mask.project_name == project_name).filter(Mask.task_id == task_id).all()

    def create(self, db:Session, mask_in:MaskBase)->Mask:
        db_mask = Mask(project_name=mask_in.project_name,
                        task_id=mask_in.task_id,
                        type=mask_in.type,
                        class_code=mask_in.class_code,
                        points=mask_in.points)
        db.add(db_mask)
        db.commit()
        db.refresh(db_mask)
        return db_mask


mask = CRUDMask() 