from pydantic import BaseModel


class ClassesBase(BaseModel):
    code: int
    name: str
    project_name: str
    description: str
