from sqlalchemy.orm import Session

from app.models.classes import Classes
from app.schemas.classes import ClassesBase


class CRUDClasses():

    def get_all(self, db:Session, project_name:str) -> list[Classes]:
        return db.query(Classes).filter(Classes.project_name == project_name).all()
    
    def create_classes(self, db:Session, project_name:str, classes:list[ClassesBase])->None:
        for cls in classes:
            db_class = Classes(color_code=cls.color_code,
                               name=cls.name,
                               project_name=project_name,
                               description=cls.description)
            db.add(db_class)
        db.commit()
        db.refresh(db_class)

    def create_class(self, db:Session, project_name:str, cls:ClassesBase)->None:
        db_class = Classes(color_code=cls.color_code,
                            name=cls.name,
                            project_name=project_name,
                            description=cls.description)
        db.add(db_class)
        db.commit()
        db.refresh(db_class)
    
    def delete_classes(self, db:Session, project_name:str) -> list[Classes]:
        ...

    def delete_class(self, db:Session) -> Classes:
        ...
    
    def update(self, db:Session):
        ...

classes = CRUDClasses()