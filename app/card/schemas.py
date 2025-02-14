import re
from typing import List
from pydantic import BaseModel, Field


class Card(BaseModel):
    front_card: str
    back_card: str
    topic_id: int
    info: dict # Добавляем обязательное поле info

class CardFilter(BaseModel):
    id: int
    topic_id: int