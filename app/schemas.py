import pydantic
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Demo


class Schema(pydantic.BaseModel):
    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


DemoDetail = pydantic_model_creator(Demo)
DemoEdit = pydantic_model_creator(Demo, exclude_readonly=True)
