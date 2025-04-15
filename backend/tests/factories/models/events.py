import datetime

from faker import Faker
from polyfactory import AsyncPersistenceProtocol
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from src.core.enums import EventTypeEnum, StatusTypeEnum
from src.models import Event


class AsyncPersistenceHandler(AsyncPersistenceProtocol[Event]):
    pass


class EventFactory(SQLAlchemyFactory[Event]):
    __faker__ = Faker()
    __async_persistence__ = AsyncPersistenceHandler

    @classmethod
    def event_type(cls) -> EventTypeEnum:
        return EventTypeEnum(cls.__random__.choice(list(EventTypeEnum)))

    @classmethod
    def status(cls) -> StatusTypeEnum:
        return StatusTypeEnum(cls.__random__.choice(list(StatusTypeEnum)))

    @classmethod
    def performance_id(cls) -> None:
        return None

    @classmethod
    def date(cls) -> datetime.date:
        return datetime.date.today() + datetime.timedelta(days=cls.__random__.randint(1, 5))
