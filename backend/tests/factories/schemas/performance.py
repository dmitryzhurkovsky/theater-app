import random

from faker import Faker
from polyfactory.factories import pydantic_factory

from src.core.enums import CategoryTypeEnum, GenreTypeEnum
from src.core.schemas import PerformanceCreate


class PerformanceCreateSchemaFactory(pydantic_factory.ModelFactory[PerformanceCreate]):
    __faker__ = Faker()

    @classmethod
    def title(cls) -> str:
        return cls.__faker__.pystr(max_chars=30)

    @classmethod
    def description(cls) -> str:
        return cls.__faker__.text(max_nb_chars=1024)

    @classmethod
    def about_author(cls) -> str:
        return cls.__faker__.text(max_nb_chars=1024)

    @classmethod
    def annotation(cls) -> str:
        return cls.__faker__.text(max_nb_chars=1024)

    @classmethod
    def genre(cls) -> list[GenreTypeEnum]:
        return random.sample(list(GenreTypeEnum), k=random.randint(1, len(GenreTypeEnum)))

    @classmethod
    def category(cls) -> CategoryTypeEnum:
        return random.choice(list(CategoryTypeEnum))
