from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from dao.session_maker import SessionDep
from auth.dependencies import get_current_user
from auth.models import User
from .dao import LastRecentlyDAO

router = APIRouter(prefix="/last_recently", tags=["last_recently"])

@router.get("")
async def get_last_pages(
    session: AsyncSession = SessionDep,
    current_user: User = Depends(get_current_user)
) -> List[str]:
    history = await LastRecentlyDAO.get_user_history(
        session=session, 
        user_id=current_user.id
    )
    return history[0].last_links if history else []

@router.post("/{page_url}")
async def add_recent_page(
    page_url: str,
    session: AsyncSession = SessionDep,
    current_user: User = Depends(get_current_user)
) -> List[str]:
    await LastRecentlyDAO.add_page(
        session=session,
        user_id=current_user.id,
        page_url=page_url
    )
    return await get_last_pages(session=session, current_user=current_user)

