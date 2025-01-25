from fastapi import APIRouter, Depends, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from course.schemas import Course, CourseCreate, CourseFilter
from card.schemas import Card
from topic.schemas import Topic
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

with open("course/testing_data.json", "r") as file:
    data = json.load(file)

router = APIRouter(prefix='/course', tags=['Course'])

@router.post("/create_course/", summary="создание курса")
async def create_course(
    course_data: CourseCreate, 
    current_user: User = Depends(get_current_user), 
    session: AsyncSession = TransactionSessionDep
):
    course_dict = course_data.model_dump()
    # Сохраняем значение link перед удалением
    course_link = course_dict["link"]
    del course_dict["link"]
    
    with open("course/testing_data.json", "r") as file:
        data = json.load(file)
    
    # Добавляем link обратно перед созданием объекта Course
    course_dict["link"] = course_link
    
    # Добавление курса в БД
    course = await CourseDAO.add(session=session, values=Course(**course_dict))
    #print(Course.model_validate(course_dict))
    
    # Добавление топиков и карточек в БД
    for topic_name, topic_data in data["course"]["topics"].items():
        # Создаем модель TopicCreate
        topic_create = TopicCreate(
            name=topic_data["name"],
            text=topic_data["text"],
            course_id=course.id
        )
        
        try:
            # Создаем топик
            topic = await TopicDAO.add(session=session, values=topic_create)
            
            # Проверяем наличие карточек
            cards_data = topic_data.get("cards", [])
            
            # Добавляем карточки если они есть
            if cards_data:
                for card_data in cards_data:
                    if card_data:  # Проверяем что карточка не пустая
                        for card_key, card_value in card_data.items():
                            card = Card(
                                front_card=card_value["answer"],
                                back_card=card_value["question"],
                                topic_id=topic.id,
                                info="Default card information"
                            )
                            await CardDAO.add(session=session, values=card)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Course created successfully"}

@router.get("/get_courses/{module_id}", summary="получение всех курсов по module_id")
async def get_courses(
    module_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    module = await ModuleDAO.find_one_or_none_by_id(module_id, session)
    if not module:
        raise HTTPException(status_code=404, detail="Модуль не найден")
    
    sphere = await SphereDAO.find_one_or_none_by_id(module.sphere_id, session)
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к модулю")
    
    courses = await CourseDAO.get_courses_by_module(session=session, module_id=module_id)
    return {"courses": courses}

@router.get("/get_course/{course_id}", summary="Получение курса по id")
async def get_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    # Получаем курс
    course = await CourseDAO.find_one_or_none_by_id(course_id, session)
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    
    # Проверяем доступ через модуль и сферу
    module = await ModuleDAO.find_one_or_none_by_id(course.module_id, session)
    sphere = await SphereDAO.find_one_or_none_by_id(module.sphere_id, session)
    
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к курсу")
        
    return {"course": course}