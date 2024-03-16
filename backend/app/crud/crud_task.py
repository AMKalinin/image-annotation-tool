from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.models.task import Task
from app.schemas.task import TaskBase
from app.utils.project import ProjectWorker

class CRUDTask():

    def get_all(self, db:Session, project_name:str) -> list[Task]:
        return db.query(Task).filter(Task.project_name == project_name).all()

    def create_tasks(self, db:Session, project_name:str, images:list[UploadFile])->Task:
        img_info_dict = self.create_file(project_name, images)
        db_tasks = self.create_db(db, project_name, images, img_info_dict)
        return db_tasks

    def create_file(self, project_name:str, images:list[UploadFile])->dict:
        prj_worker = ProjectWorker(project_name)
        img_info_dict = prj_worker.add_tasks(images)
        return img_info_dict

    def create_db(self, db:Session, 
                  project_name:str,
                  images:list[UploadFile],
                  img_info_dict:list[int]):
        
        for index, image in enumerate(images):
            db_task = Task(id=index,
                            project_name=project_name,
                            file_name=image.filename,
                            width=img_info_dict[index][1],
                            height=img_info_dict[index][2],
                            layers_count=img_info_dict[index][0],
                            status_name='to_do')
            db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def get_by_id(self, db:Session, project_name:str, task_id:int) -> Task:
        return db.query(Task).filter(Task.project_name == project_name).filter(Task.id == task_id).first()
    
    def get_icon(self, project_name:str, task_id:int)-> bytes:
        prj_worker = ProjectWorker(project_name)
        icon_bytes = prj_worker.get_task_icon(task_id)
        return icon_bytes
    
    def get_tile(self, 
                 project_name:str, 
                 task_id:int, 
                 layer_number:int, 
                 x:int, y:int) -> bytes:
        prj_worker = ProjectWorker(project_name)
        icon_bytes = prj_worker.get_task_tail(task_id, layer_number, x, y)
        return icon_bytes


task = CRUDTask() 