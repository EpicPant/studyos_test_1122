from dao.base import BaseDAO
from sqlalchemy import select
from last_recently.model import last_recent
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

class LastRecentlyDAO(BaseDAO):
    model = last_recent

    @classmethod
    async def get_user_history(cls, session: AsyncSession, user_id: int) -> List[last_recent]:
        query = select(cls.model).where(
            cls.model.user_id == user_id
        ).order_by(cls.model.created_at.desc()).limit(5)
        
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add_page(cls, session: AsyncSession, user_id: int, page_url: str):
        # Получаем текущее количество записей
        count_query = select(cls.model).where(cls.model.user_id == user_id)
        result = await session.execute(count_query)
        current_records = result.scalars().all()

        # Если записей больше 4, удаляем самую старую
        if len(current_records) >= 5:
            oldest_record = current_records[-1]
            await session.delete(oldest_record)

        # Добавляем новую запись
        new_page = last_recent(user_id=user_id, last_links=[page_url])
        session.add(new_page)
        await session.commit()
