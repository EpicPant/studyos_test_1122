from typing import List
from pydantic import BaseModel, Field, HttpUrl


class CourseBase(BaseModel):
    name: str = Field(..., description="Название курса")

class CourseCreate(CourseBase):
    #user_id: int = Field(..., description="Идентификатор пользователя, которому принадлежит курс")
    link: HttpUrl = Field(..., description="ссылка на материал курса(пока только Youtube)")
    module_id: int = Field(..., description="Идентификатор модуля, в котором будет курс")

class Course(CourseBase):
    topics: List[int] = Field(default=[], description="Список идентификаторов топиков, связанных с этим курсом")
    module_id: int = Field(..., description="Идентификатор модуля, в котором будет курс")

    class Config:
        orm_mode = True

class CourseFilter(BaseModel):
    id: int = Field(..., description="ID курса для фильтрации")
    module_id: int = Field(..., description="ID модуля для фильтрации курсов")
        