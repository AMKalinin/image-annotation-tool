from pydantic import BaseModel


class MaskBase(BaseModel):
    project_name: str
    task_id: int
    type: str
    class_code: int
    points: str


class MaskOut(BaseModel):
    id: int
    project_name: str
    task_id: int
    type: str
    class_code: int
    points: str
    color_code: str