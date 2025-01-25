from dao.base import BaseDAO
from course.models import Course
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class CourseDAO(BaseDAO):
    model = Course

    @classmethod
    async def get_courses_by_module(cls, session: AsyncSession, module_id: int):
        query = (
            select(cls.model)
            .filter(cls.model.module_id == module_id)
            .options(selectinload(cls.model.topics))
        )
        result = await session.execute(query)
        return result.scalars().unique().all()