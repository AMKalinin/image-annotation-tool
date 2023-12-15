from pydantic import BaseModel


class TaskBase(BaseModel):
    id: int
    project_name: str
    file_name: str
    width: int
    height: int
    layers_count: int = 1
    status: str 