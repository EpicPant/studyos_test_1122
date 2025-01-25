import re
from typing import List, Optional
from pydantic import BaseModel

class TopicBase(BaseModel):
    name: str
    text: str
    course_id: int

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: int
    cards: Optional[List[int]] = []

class TopicFilter(BaseModel):
    course_id: int
