from typing import TYPE_CHECKING

from sqlalchemy import text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dao.database import Base, str_uniq

if TYPE_CHECKING:
    from app.card.models import Card
    from app.course.models import Course

class Topic(Base):
    name: Mapped[str]
    text: Mapped[str]
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="topic", cascade="all, delete-orphan")  # Исправлено на cards
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey('courses.id'))
    course: Mapped["Course"] = relationship("Course", back_populates="topics") 
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"