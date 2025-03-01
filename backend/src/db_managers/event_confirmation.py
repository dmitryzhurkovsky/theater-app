from src.db_managers.base import BaseDatabaseManager
from src.models import EventConfirmation


class EventConfirmationManager(BaseDatabaseManager):
    model = EventConfirmation
