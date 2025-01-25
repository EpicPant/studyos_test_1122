from fastapi import APIRouter, Depends, Response, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from module.models import Module as ModuleDB
from module.schemas import ModuleCreate, ModuleFilter  # Добавить импорт схемы
from sphere.dao import SphereDAO
from module.dao import ModuleDAO
from auth.models import User
from auth.dependencies import get_current_user
from dao.session_maker import TransactionSessionDep




router = APIRouter(prefix='/module', tags=['Module'])

@router.post("/create_module/", summary="Создание Модуля")
async def create_module(
    module_data: ModuleCreate, 
    current_user: User = Depends(get_current_user), 
    session: AsyncSession = TransactionSessionDep
):
    module_dict = module_data.model_dump()
    module_dict["user_id"] = current_user.id
    module = await ModuleDAO.add(session=session, values=ModuleCreate.model_validate(module_dict))
    return {"message": "Module added"}

@router.get("/get_moudle/{module_id}")
async def get_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    # Получаем модуль
    module = await ModuleDAO.find_one_or_none_by_id(module_id, session)
    if not module:
        raise HTTPException(status_code=404, detail="Модуль не найден")
    
    # Получаем сферу для проверки доступа
    sphere = await SphereDAO.find_one_or_none_by_id(module.sphere_id, session)
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к модулю")
        
    return {"module": module}

@router.get("/{sphere_id}/get_modules/")
async def get_modules(
    sphere_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = TransactionSessionDep
):
    # Проверяем доступ к сфере
    sphere = await SphereDAO.find_one_or_none_by_id(sphere_id, session)
    if not sphere:
        raise HTTPException(status_code=404, detail="Сфера не найдена")
        
    if sphere.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к сфере")
    
    # Получаем модули сферы
    filters = ModuleFilter(sphere_id=sphere_id)
    modules = await ModuleDAO.find_all(session=session, filters=filters)
    return {"modules": modules}