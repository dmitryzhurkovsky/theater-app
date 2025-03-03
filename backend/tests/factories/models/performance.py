import random

from faker import Faker
from polyfactory import AsyncPersistenceProtocol
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from src.core.enums import CategoryTypeEnum, GenreTypeEnum
from src.models import Performance


class AsyncPersistenceHandler(AsyncPersistenceProtocol[Performance]):
    pass


class PerformanceFactory(SQLAlchemyFactory[Performance]):
    __faker__ = Faker()
    __async_persistence__ = AsyncPersistenceHandler

    @classmethod
    def title(cls) -> str:
        return cls.__faker__.pystr(max_chars=30)

    @classmethod
    def description(cls) -> str:
        return cls.__faker__.pystr(max_chars=1024)

    @classmethod
    def about_author(cls) -> str:
        return cls.__faker__.pystr(max_chars=1024)

    @classmethod
    def annotation(cls) -> str:
        return cls.__faker__.pystr(max_chars=1024)

    @classmethod
    def genre(cls) -> list[GenreTypeEnum]:
        return random.sample(list(GenreTypeEnum), k=random.randint(1, len(GenreTypeEnum)))

    @classmethod
    def category(cls) -> CategoryTypeEnum:
        return cls.__random__.choice(list(CategoryTypeEnum))

    @classmethod
    def age(cls) -> int:
        return cls.__faker__.pyint(min_value=0, max_value=100)
