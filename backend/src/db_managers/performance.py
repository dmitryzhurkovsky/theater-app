from src.db_managers.base import BaseDatabaseManager
from src.models import Performance


class PerformanceManager(BaseDatabaseManager):
    model = Performance
