from typing import Optional
from dao.base import BaseDAO
from module.models import Module
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


class ModuleDAO(BaseDAO):
    model = Module

    

    