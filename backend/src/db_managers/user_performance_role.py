from src.db_managers.base import BaseDatabaseManager
from src.models import UserPerformanceRoleRelationship


class UserPerformanceRoleManager(BaseDatabaseManager):
    model = UserPerformanceRoleRelationship
