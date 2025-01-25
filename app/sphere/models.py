from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dao.database import Base

if TYPE_CHECKING:
    from auth.models import User
    from module.models import Module

class Sphere(Base):
    name: Mapped[str]
    icon: Mapped[str]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates="spheres")
    modules: Mapped[list["Module"]] = relationship("Module", back_populates="sphere")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
