import random
from datetime import date, timedelta

from faker import Faker
from polyfactory.factories import pydantic_factory

from src.core.enums import GenderTypeEnum, UserRoleTypeEnum
from src.core.schemas import UserBase, UserCreate, UserRegister


class UserBaseSchemaFactory(pydantic_factory.ModelFactory[UserBase]):
    __faker__ = Faker()

    @classmethod
    def gender(cls) -> GenderTypeEnum:
        return random.choice(list(GenderTypeEnum))

    @classmethod
    def user_roles(cls) -> list[UserRoleTypeEnum]:
        return random.sample(list(UserRoleTypeEnum), k=random.randint(1, len(UserRoleTypeEnum)))


class UserRegisterSchemaFactory(UserBaseSchemaFactory):
    __model__ = UserRegister

    @classmethod
    def password(cls) -> str:
        return cls.__faker__.password()


class UserCreateSchemaFactory(UserBaseSchemaFactory):
    __model__ = UserCreate

    @classmethod
    def free_dates(cls) -> list[date]:
        return [date.today() + timedelta(days=i) for i in range(1, random.randint(2, 10))]
