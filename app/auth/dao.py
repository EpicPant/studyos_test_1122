from dao.base import BaseDAO
from auth.models import User


class UsersDAO(BaseDAO):
    model = User
