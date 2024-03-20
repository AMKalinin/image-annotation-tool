from pydantic import BaseModel
import datetime


class ProjectOut(BaseModel):
    name: str
    create_date: datetime.date
    last_update: datetime.date
    creator: str
    status_name: str
    description: str | None


class ProjectIn(BaseModel):
    name: str
    create_date: datetime.date = datetime.date.today()
    last_update: datetime.date = datetime.date.today()
    creator: str
    description: str | None
