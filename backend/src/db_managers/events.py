from src.db_managers.base import BaseDatabaseManager
from src.models import Event


class EventsManager(BaseDatabaseManager):
    model = Event
