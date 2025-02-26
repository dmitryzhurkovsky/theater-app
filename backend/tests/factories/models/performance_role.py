from faker import Faker
from polyfactory import AsyncPersistenceProtocol
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from src.models import PerformanceRole


class AsyncPersistenceHandler(AsyncPersistenceProtocol[PerformanceRole]):
    pass


class PerformanceRoleFactory(SQLAlchemyFactory[PerformanceRole]):
    __faker__ = Faker()
    __async_persistence__ = AsyncPersistenceHandler

    @classmethod
    def title(cls) -> str:
        return cls.__faker__.pystr(max_chars=30)
