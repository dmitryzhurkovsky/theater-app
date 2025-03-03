from src.db_managers.base import BaseDatabaseManager
from src.models import Event


class EventManager(BaseDatabaseManager):
    model = Event
