from typing import Any

from src.core.database.utils import get_by
from src.db_managers.base import BaseDatabaseManager
from src.models import User


class UserManager(BaseDatabaseManager):
    model = User

    async def get_by_email(self, filters: dict[str, Any]) -> User:
        stmt = get_by(self.model, query=self.base_query, criteria=filters)
        return await self.session.scalar(stmt)
