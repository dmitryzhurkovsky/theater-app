from abc import ABC, abstractmethod

from src.core.database.db import postgres_async_session
from src.services import BaseService


class AbstractUnitOfWork(ABC):
    service = type[BaseService]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork:
    def __init__(self):
        self.session_factory = postgres_async_session

    async def __aenter__(self):
        self.session = self.session_factory()

    async def __aexit__(self, *args, **kwargs):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
