from pydantic import BaseModel
import datetime


class ProjectBase(BaseModel):
    name: str
    create_date: datetime.date = datetime.date.today()
    last_update: datetime.date = datetime.date.today()
    creator: str
    status: str
    description: str | None
