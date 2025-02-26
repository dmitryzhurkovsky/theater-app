from typing import Any

from faker import Faker
from polyfactory import AsyncPersistenceProtocol
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from src.core.enums import GenderTypeEnum, UserRoleTypeEnum
from src.models import User
from src.utils.security.password_handler import make_password_hash


class AsyncPersistenceHandler(AsyncPersistenceProtocol[User]):
    pass


class UserFactory(SQLAlchemyFactory[User]):
    __faker__ = Faker()
    __async_persistence__ = AsyncPersistenceHandler

    @classmethod
    def email(cls) -> str:
        return cls.__faker__.email()

    @classmethod
    def gender(cls) -> GenderTypeEnum:
        return cls.__random__.choice(list(GenderTypeEnum))

    @classmethod
    def user_roles(cls) -> list[UserRoleTypeEnum]:
        return cls.__random__.sample(list(UserRoleTypeEnum), k=cls.__random__.randint(1, len(UserRoleTypeEnum)))

    @classmethod
    def phone_number(cls) -> str:
        return cls.__faker__.phone_number()

    @classmethod
    def password(cls) -> str:
        return cls.__faker__.password()

    @classmethod
    def build(cls, **kwargs: Any) -> User:
        user_instance = super().build(**kwargs)
        user_instance.password = make_password_hash(user_instance.password)
        return user_instance
