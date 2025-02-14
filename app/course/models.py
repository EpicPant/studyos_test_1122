from typing import TYPE_CHECKING

from sqlalchemy import text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dao.database import Base

if TYPE_CHECKING:
    from topic.models import Topic
    from module.models import Module

class Course(Base):
    name: Mapped[str]

    module_id: Mapped[int] = mapped_column(Integer, ForeignKey('modules.id'))
    module: Mapped["Module"] = relationship("Module", back_populates="courses")
    topics: Mapped[list["Topic"]] = relationship("Topic", back_populates="course", lazy="joined", cascade="all, delete-orphan")  # Связь с темами

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
