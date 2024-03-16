from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.status import Status  #it is necessary for the relationship
from app.models.classes import Classes  #it is necessary for the relationship
from app.schemas.project import ProjectBase
from app.utils.project import ProjectWorker

class CRUDProject():

    def get_all(self, db:Session)->list[Project]:
        return db.query(Project).all()

    def create(self, db:Session, project_in:ProjectBase) -> Project:
        db_project = self.create_db(db, project_in)
        self.create_file(project_in)
        return db_project
    
    def create_db(self,db:Session, project_in:ProjectBase)->Project:
        db_project = Project(name = project_in.name,
                             create_date = project_in.create_date,
                             last_update = project_in.last_update,
                             creator = project_in.creator,
                             status_name = 'to_do',                 # убрать подобные штуки
                             description = project_in.description)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    def create_file(self, project_in:ProjectBase) -> None:
            prj_worker = ProjectWorker(project_in.name)
            prj_worker.create_project()
    
    def get_by_name(self, db:Session, name:str) -> Project:
        return db.query(Project).filter(Project.name == name).first()
    
    def update(self, db:Session, db_project:Project, project_in:ProjectBase) -> Project:
        db_project.last_update = project_in.last_update
        db.commit()
        return db_project
    
    def delete(self, db:Session, db_project:Project):
        db.delete(db_project)
        db.commit()
    
    def delete_by_name(self, db:Session, name:str):
        project = db.query(Project).get(name)
        db.delete(project)
        db.commit()


project = CRUDProject() 
    