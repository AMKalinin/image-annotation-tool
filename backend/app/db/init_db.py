from sqlalchemy.orm import Session

from .base_class import Base
from .session import engine
import datetime

from app.models.project import Project
from app.models.task import Task
from app.models.mask import Mask
from app.models.status import Status

def init_db():
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        with session.begin():
            status_todo = Status(name = 'to_do',
                            description = 'Project/task created')
            
            status_inprogress = Status(name = 'in_progress',
                            description = 'Project/task in progress')
            
            status_tocheck = Status(name = 'to_check',
                            description = 'Project/task wait check')
            
            status_done = Status(name = 'done',
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
            mask = Mask(id=1,
                        project_name = task.project_name,
                        task_id = task.id,
                        type = 'test',
                        class_code = 110,
                        points='12 3,14 5')
            session.add(mask)

        with session.begin():
            session.delete(mask)

        with session.begin():
            session.delete(task)
            
        with session.begin():
            session.delete(project)
