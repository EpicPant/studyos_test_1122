from dao.base import BaseDAO
from topic.models import Topic


class TopicDAO(BaseDAO):
    model = Topic