from faker import Faker
from polyfactory.factories import pydantic_factory

from src.core.schemas import PerformanceRoleCreate


class PerformanceRoleCreateSchemaFactory(pydantic_factory.ModelFactory[PerformanceRoleCreate]):
    __faker__ = Faker()

    @classmethod
    def title(cls) -> str:
        return cls.__faker__.pystr(max_chars=30)
