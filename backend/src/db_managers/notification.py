from src.db_managers.base import BaseDatabaseManager
from src.models import Notification


class NotificationManager(BaseDatabaseManager):
    model = Notification
