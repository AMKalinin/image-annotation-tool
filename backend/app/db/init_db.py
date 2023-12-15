from sqlalchemy.orm import Session

from .base_class import Base
from .session import engine
import datetime

from app.models.project import Project
from app.models.task import Task
from app.models.mask import Mask

def init_db():
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        with session.begin():
            project = Project(name = 'asddas',
                    create_date = datetime.date.today(),
                    last_update = datetime.date.today(),
                    creator = 'i',
                    status = 'OK',
                    description = 'description')
            session.add(project)

        with session.begin():
            task = Task(id=1,
                        project_name = project.name,
                        file_name = 'file name',
                        width = 100,
                        height = 150, 
                        layers_count = 4,
                        status = 'ok')
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
