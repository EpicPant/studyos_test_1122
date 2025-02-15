from typing import List
from fastapi import APIRouter, Response, Depends
from auth.dependencies import get_current_user
from auth.models import User
from exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from auth.auth import authenticate_user, create_access_token, set_tokens
from auth.dao import UsersDAO
from auth.schemas import SUserRegister, SUserAuth, EmailModel, SUserAddDB, SUserInfo
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import check_refresh_token


from dao.session_maker import TransactionSessionDep, SessionDep

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register")
async def register_user(user_data: SUserRegister, session: AsyncSession = TransactionSessionDep) -> dict:
    user = await UsersDAO.find_one_or_none(session=session, filters=EmailModel(email=user_data.email))
    if user:
        raise UserAlreadyExistsException
    user_data_dict = user_data.model_dump()
    del user_data_dict['confirm_password']
    await UsersDAO.add(session=session, values=SUserAddDB(**user_data_dict))
    return {'message': f'Вы успешно зарегистрированы!'}


@router.post("/login")
async def auth_user(response: Response, user_data: SUserAuth, session: AsyncSession = SessionDep):
    check = await authenticate_user(session=session, email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    else:
        user = await UsersDAO(session).find_one_or_none(
            session=session,
            filters=EmailModel(email=user_data.email)
        )
        set_tokens(response, user.id)
    return {'ok': True, 'message': 'Авторизация успешна!'}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")
    response.delete_cookie("user_refresh_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me")
async def get_me(user_data: User = Depends(get_current_user)) -> SUserInfo:
    print(user_data)
    return SUserInfo.model_validate(user_data)

@router.post("/refresh")
async def process_refresh_token(
        response: Response,
        user: User = Depends(check_refresh_token)
):
    set_tokens(response, user.id)
    return {"message": "Токены успешно обновлены"}


'''@router.get("/all_users/")
async def get_all_users(session: AsyncSession = SessionDep,
                        user_data: User = Depends(get_current_admin_user)) -> List[SUserInfo]:
    return await UsersDAO.find_all(session=session, filters=None)'''
