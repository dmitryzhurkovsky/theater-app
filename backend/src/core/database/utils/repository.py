from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from src.core.database.db import postgres_async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def get(self, filter_by: dict = None):
        async with postgres_async_session() as session:
            statement = select(self.model).filter_by(**filter_by)
            result = await session.execute(statement)
            return result.scalar_one().to_read_model()

    async def all(self, filter_by: dict = None):
        async with postgres_async_session() as session:
            statement = select(self.model)
            result = await session.execute(statement)
            return result.scalars()

    async def create(self, data: dict) -> UUID:
        async with postgres_async_session() as session:
            statement = insert(self.model).values(**data).returning(self.model)
            result = await session.execute(statement)
            await session.commit()
            return result.scalar_one()
