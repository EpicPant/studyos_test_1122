from typing import TYPE_CHECKING

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dao.database import Base, str_uniq

if TYPE_CHECKING:
    from app.sphere.models import Sphere


class User(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]

    spheres: Mapped[list["Sphere"]] = relationship("Sphere", back_populates="user", lazy="joined")
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
