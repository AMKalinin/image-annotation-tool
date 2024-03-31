from sqlalchemy.orm import Session

from app.models.mask import Mask
from app.schemas.mask import MaskBase, MaskOut
from app.models.classes import Classes  #it is necessary for the relationship

class CRUDMask():
    def get_all(self, db:Session, project_name:str, task_id:int)-> list[MaskOut]:
        # TODO rename a, m, c
        a = db.query(Mask, Classes
                       ).filter(Mask.class_code == Classes.code
                        ).filter(Mask.project_name == project_name
                        ).where(Mask.task_id == task_id).all()
        res = []
        for m, c in a:
            res.append(MaskOut(id=m.id,
                               project_name=m.project_name,
                               task_id=m.task_id,
                               type=m.type,
                               class_code=m.class_code,
                               points=m.points,
                               color_code=c.color_code))
        return res

    def create(self, db:Session, mask_in:MaskBase)->Mask:
        db_mask = Mask(project_name=mask_in.project_name,
                        task_id=mask_in.task_id,
                        type=mask_in.type,
                        class_code=mask_in.class_code,
                        points=mask_in.points)
        
        db.add(db_mask)
        db.commit()
        db.refresh(db_mask)
        
        classes = db.query(Classes).filter( Classes.code == db_mask.class_code).one()

        mask_out =MaskOut(id=db_mask.id,
                        project_name=db_mask.project_name,
                        task_id=db_mask.task_id,
                        type=db_mask.type,
                        class_code=db_mask.class_code,
                        points=db_mask.points,
                        color_code=classes.color_code)
        return mask_out
    
    def delete_by_id(self, db:Session, project_name:str, task_id:int, mask_id:int):
        mask = db.query(Mask).get({'project_name':project_name,
                                   'task_id': task_id,
                                   'id': mask_id
                                   })
        db.delete(mask)
        db.commit()

    def change_class_code(self, db:Session, project_name:str, task_id:int, mask_id:int, new_class_code:int):
        mask = db.query(Mask).get({'project_name':project_name,
                                'task_id': task_id,
                                'id': mask_id
                                })
        mask.class_code = new_class_code
        db.commit()

mask = CRUDMask() 