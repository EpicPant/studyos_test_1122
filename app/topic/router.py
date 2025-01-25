from fastapi import APIRouter, Depends, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from course.schemas import Course, CourseCreate, CourseFilter
from card.schemas import Card
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
import json
from topic.dao import TopicDAO
from card.dao import CardDAO
from course.dao import CourseDAO
from topic.models import Topic
from topic.schemas import TopicCreate, Topic

router = APIRouter(prefix='/topic', tags=['Topic'])

@router.get("/get_topic/{topic_id}")
async def get_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    # Получаем топик
    topic = await TopicDAO.find_one_or_none_by_id(topic_id, session)
    if not topic:
        raise HTTPException(status_code=404, detail="Топик не найден")
    
    # Получаем курс
    course = await CourseDAO.find_one_or_none_by_id(topic.course_id, session)
    # Получаем модуль
    module = await ModuleDAO.find_one_or_none_by_id(course.module_id, session)
    # Получаем сферу
    sphere = await SphereDAO.find_one_or_none_by_id(module.sphere_id, session)
    
    # Проверяем доступ
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к топику")
        
    return {"topic": topic}

@router.get("/get_topics/{course_id}", summary="Получение топиков курса")
async def get_topics(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    # Проверяем доступ через иерархию
    course = await CourseDAO.find_one_or_none_by_id(course_id, session)
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    
    module = await ModuleDAO.find_one_or_none_by_id(course.module_id, session)
    sphere = await SphereDAO.find_one_or_none_by_id(module.sphere_id, session)
    
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к курсу")
    
    # Получаем топики
    filters = TopicFilter(course_id=course_id)
    topics = await TopicDAO.find_all(session=session, filters=filters)
    return {"topics": topics}

