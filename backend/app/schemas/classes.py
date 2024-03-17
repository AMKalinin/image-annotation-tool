from pydantic import BaseModel, model_validator
import json


class ClassesBase(BaseModel):
    color_code: str
    name: str
    project_name: str
    description: str

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
