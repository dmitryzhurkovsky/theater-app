from src.db_managers.base import BaseDatabaseManager
from src.models import PerformanceRole


class PerformanceRoleDatabaseManager(BaseDatabaseManager):
    model = PerformanceRole
