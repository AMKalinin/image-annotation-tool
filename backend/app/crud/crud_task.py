from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskBase
from app.utils.project import ProjectWorker

class CRUDTask():

    def get_all(self, db:Session, project_name:str) -> list[Task]:
        return db.query(Task).filter(Task.project_name == project_name).all()

    def create(self, db:Session, task_in:TaskBase)->Task:
        db_task = Task(id=task_in.id,
                        project_name=task_in.project_name,
                        file_name=task_in.file_name,
                        width=task_in.width,
                        height=task_in.height,
                        layers_count=task_in.layers_count,
                        status_name=task_in.status_name)
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