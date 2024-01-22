from src.db_managers.base import BaseDatabaseManager
from src.models import User


class UserManager(BaseDatabaseManager):
    model = User
