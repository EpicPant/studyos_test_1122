from dao.base import BaseDAO
from card.models import Card


class CardDAO(BaseDAO):
    model = Card