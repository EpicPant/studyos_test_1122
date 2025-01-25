import re
from typing import List
from pydantic import BaseModel, Field


class SphereBase(BaseModel):
    name: str = Field(..., description="Название сферы")
    icon: str = Field(..., description="Иконка сферы")

class SphereCreate(SphereBase):
    user_id: int = Field(..., description="id_пользователя")

class Sphere(SphereBase):
    user_id: int = Field(..., description="Идентификатор пользователя, которому принадлежит сфера")
    courses: List[int] = Field(default=[], description="Список идентификаторов курсов, связанных с этой сферой")

    class Config:
        orm_mode = True

class SphereFilter(BaseModel):
    user_id: int