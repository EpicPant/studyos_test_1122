from fastapi import APIRouter, Depends, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from course.schemas import Course, CourseCreate, CourseFilter
from card.schemas import Card, CardFilter
from topic.schemas import Topic, TopicFilter
from sphere.dao import SphereDAO
from course.dao import CourseDAO
from module.dao import ModuleDAO
from card.dao import CardDAO
from services.course import Course as CourseAI
from services.extract_audio import download_audio
from auth.models import User
from auth.dependencies import get_current_user
from dao.session_maker import TransactionSessionDep
from topic.dao import TopicDAO
from card.dao import CardDAO
from course.dao import CourseDAO
from topic.models import Topic
from topic.schemas import TopicCreate, Topic

router = APIRouter(prefix='/card', tags=['Card'])

@router.get("/get_card/{card_id}", summary="Получение карточки по ID")
async def get_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    card = await CardDAO.find_one_or_none_by_id(card_id, session)
    if not card:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    
    # Проверка доступа через цепочку зависимостей
    topic = await TopicDAO.find_one_or_none_by_id(card.topic_id, session)
    course = await CourseDAO.find_one_or_none_by_id(topic.course_id, session)
    module = await ModuleDAO.find_one_or_none_by_id(course.module_id, session)
    sphere = await SphereDAO.find_one_or_none_by_id(module.sphere_id, session)
    
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к карточке")
        
    return {"card": card}

@router.get("/get_cards/{topic_id}", summary="Получение всех карточек топика")
async def get_cards(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    # Проверка доступа
    topic = await TopicDAO.find_one_or_none_by_id(topic_id, session)
    if not topic:
        raise HTTPException(status_code=404, detail="Топик не найден")
        
    course = await CourseDAO.find_one_or_none_by_id(topic.course_id, session)
    module = await ModuleDAO.find_one_or_none_by_id(course.module_id, session)
    sphere = await SphereDAO.find_one_or_none_by_id(module.sphere_id, session)
    
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к карточкам")
    
    # Получение карточек
    filters = CardFilter(topic_id=topic_id)
    cards = await CardDAO.find_all(session=session, filters=filters)
    return {"cards": cards}

@router.delete("/delete_card/{card_id}", summary="Удаление карточки")
async def delete_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    card = await CardDAO.find_one_or_none_by_id(card_id, session)
    if not card:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    
    # Проверка доступа через цепочку зависимостей
    topic = await TopicDAO.find_one_or_none_by_id(card.topic_id, session)
    course = await CourseDAO.find_one_or_none_by_id(topic.course_id, session)
    module = await ModuleDAO.find_one_or_none_by_id(course.module_id, session)
    sphere = await SphereDAO.find_one_or_none_by_id(module.sphere_id, session)
    
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к карточке")
    
    card_filter = CardFilter(id=card_id, topic_id=card.topic_id)
    await CardDAO.delete(session=session, filter=card_filter)
    return {"message": "Карточка удалена"}

@router.put("/update_card/{card_id}", summary="Обновление карточки")
async def update_card(
    card_id: int,
    card: Card,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    old_card = await CardDAO.find_one_or_none_by_id(card_id, session)
    if not old_card:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    
    # Проверка доступа через цепочку зависимостей
    topic = await TopicDAO.find_one_or_none_by_id(card.topic_id, session)
    course = await CourseDAO.find_one_or_none_by_id(topic.course_id, session)
    module = await ModuleDAO.find_one_or_none_by_id(course.module_id, session)
    sphere = await SphereDAO.find_one_or_none_by_id(module.sphere_id, session)
    
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к карточке")
    
    # Обновление карточки
    update_filter = CardFilter(id=card_id, topic_id=card.topic_id)
    new_value = card.model_dump()
    await CardDAO.update(session=session, filters=update_filter, values=new_value)
    return {"message": "Карточка обновлена"}