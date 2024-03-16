from sqlalchemy.orm import Session

from app.models.classes import Classes


class CRUDClasses():

    def get_all(self, db:Session, project_name:str) -> list[Classes]:
        return db.query(Classes).filter(Classes.project_name == project_name)
    
    def create_classes(self, db:Session):
        ...

    def create_class(self, db:Session):
        ...
    
    def delete_classes(self, db:Session):
        ...

    def delete_class(self, db:Session):
        ...
    
    def update(self, db:Session):
        ...

classes = CRUDClasses()