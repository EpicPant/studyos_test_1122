from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dao.database import Base

if TYPE_CHECKING:
    from auth.models import User
    from course.models import Course
    from sphere.models import Sphere

class Module(Base):
    name: Mapped[str]
    icon: Mapped[str]
    sphere_id: Mapped[int] = mapped_column(Integer, ForeignKey('spheres.id'))
    sphere: Mapped["Sphere"] = relationship("Sphere", back_populates="modules")
    courses: Mapped[list["Course"]] = relationship("Course", back_populates="module")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
