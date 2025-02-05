from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dao.database import Base

if TYPE_CHECKING:
    from auth.models import User
    from module.models import Module

class last_recent(Base):
    user_id: Mapped[int]
    last_links: Mapped[list[str]] = mapped_column(ARRAY(String))


    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
