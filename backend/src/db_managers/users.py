from typing import Any

from sqlalchemy.sql import Select

from src.core.database.utils import get_by
from src.core.exceptions.base import NotFoundError
from src.db_managers.base import BaseDatabaseManager
from src.models import User


class UserManager(BaseDatabaseManager):
    model = User

    async def get_by(self, filters: dict[str, Any], raise_error: bool = True) -> User | None:
        """
        Retrieves a User instance based on the provided filters.

        Args:
            filters (Dict[str, Any]): A dictionary of filters to apply to the query.
            raise_error (bool): If True, raises NotFoundError if no matching User is found. Defaults to True.

        Returns:
            User: The User instance matching the filters.

        Raises:
            NotFoundError: If no matching User is found and raise_error is True.
        """
        stmt: Select = get_by(self.model, query=self.base_query, criteria=filters)
        result = await self.session.scalar(stmt)
        if not result and raise_error:
            raise NotFoundError(detail=f"{self.model.__name__} object with {filters=} not found")
        return result
