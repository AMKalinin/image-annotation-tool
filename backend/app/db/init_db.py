from sqlalchemy.orm import Session

from .base_class import Base
from .session import engine
import datetime

from app.models.project import Project
from app.models.task import Task
from app.models.mask import Mask
from app.models.status import Status
from app.models.classes import Classes 
from app.core.const import STATUS_NAME_CREATE, STATUS_NAME_DONE, STATUS_NAME_IN_WORK, STATUS_NAME_TO_CHECK

def init_db():
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        with session.begin():
            status_todo = session.query(Status).filter(Status.name == STATUS_NAME_CREATE).first()
            if not status_todo:
                status_todo = Status(name = STATUS_NAME_CREATE,
                                description = 'Project/task created')
                
                status_inprogress = Status(name = STATUS_NAME_IN_WORK,
                                description = 'Project/task in progress')
                
                status_tocheck = Status(name = STATUS_NAME_TO_CHECK,
                                description = 'Project/task wait check')
                
                status_done = Status(name = STATUS_NAME_DONE,
                                description = 'Project/task done')
                session.add(status_todo)
                session.add(status_inprogress)
                session.add(status_tocheck)
                session.add(status_done)

        with session.begin():
            project = Project(name = 'asddas',
                    create_date = datetime.date.today(),
                    last_update = datetime.date.today(),
                    creator = 'i',
                    status_name = status_todo.name,
                    description = 'description')
            session.add(project)

        with session.begin():
            task = Task(id=1,
                        project_name = project.name,
                        file_name = 'file name',
                        width = 100,
                        height = 150, 
                        layers_count = 4,
                        status_name = status_todo.name)
            session.add(task)

        with session.begin():
            classes = Classes(name='build',
                            color_code='#FFFFFF',
                            project_name=project.name,
                            description='xnj nj yfgbcfyh')
            session.add(classes)

        with session.begin():
            mask = Mask(project_name = task.project_name,
                        task_id = task.id,
                        type = 'test',
                        class_code = classes.code,
                        points='12 3,14 5')
            session.add(mask)

        with session.begin():
            session.delete(mask)

        with session.begin():
            session.delete(task)

        with session.begin():
            session.delete(classes)
            
        with session.begin():
            session.delete(project)
