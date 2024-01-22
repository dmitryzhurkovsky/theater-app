from src.db_managers.base import BaseDatabaseManager
from src.models import TheatricalRole


class TheatricalRoleDatabaseManager(BaseDatabaseManager):
    model = TheatricalRole
