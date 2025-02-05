from fastapi import APIRouter, Depends, Response, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sphere.models import Sphere as SphereModel
from sphere.schemas import SphereBase, Sphere, SphereCreate, SphereFilter
from sphere.dao import SphereDAO
from course.dao import CourseDAO
from topic.dao import TopicDAO
from card.dao import CardDAO
from auth.models import User
from auth.dependencies import get_current_user
from dao.session_maker import TransactionSessionDep




router = APIRouter(prefix='/sphere', tags=['Sphere'])

@router.post("/create_sphere", summary="Добавление новой сферы")
async def create_sphere(
    sphere_data: SphereCreate, 
    current_user: User = Depends(get_current_user), 
    session: AsyncSession = TransactionSessionDep
):
    sphere_dict = sphere_data.model_dump()
    sphere_dict["user_id"] = current_user.id
    await SphereDAO.add(session=session, values=SphereCreate.model_validate(sphere_dict))
    return {"message": "Sphere add"}

@router.get("/get_spheres", summary="получение сфер пользователя")
async def get_spheres(
    user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    filters = SphereFilter(user_id=user.id)
    spheres = await SphereDAO.find_all(session=session, filters=filters)
    return {"spheres": spheres}

@router.get("/get_sphere/{sphere_id}", summary="Получение сферы по id")
async def get_sphere(
    sphere_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    sphere = await SphereDAO.find_one_or_none_by_id(data_id=sphere_id, session=session)
    
    if not sphere:
        raise HTTPException(
            status_code=404,
            detail="Сфера не найдена"
        )
    
    if sphere.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="У вас нет доступа к этой сфере"
        )
        
    return {"sphere": sphere}