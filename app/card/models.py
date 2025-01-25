from typing import TYPE_CHECKING

from sqlalchemy import text, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dao.database import Base, str_uniq

if TYPE_CHECKING:
    from app.topic.models import Topic

class Card(Base):
    front_card: Mapped[str] = mapped_column(Text)
    back_card: Mapped[str] = mapped_column(Text)
    info: Mapped[dict] = mapped_column(JSON)

    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey('topics.id'))
    topic: Mapped["Topic"] = relationship("Topic", back_populates="cards")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"