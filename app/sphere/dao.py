from typing import Optional
from dao.base import BaseDAO
from sphere.models import Sphere
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


class SphereDAO(BaseDAO):
    model = Sphere

    
