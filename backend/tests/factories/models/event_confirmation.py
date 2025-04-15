from faker import Faker
from polyfactory import AsyncPersistenceProtocol
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from src.models import EventConfirmation


class AsyncPersistenceHandler(AsyncPersistenceProtocol[EventConfirmation]):
    pass


class EventConfirmationFactory(SQLAlchemyFactory[EventConfirmation]):
    __faker__ = Faker()
    __async_persistence__ = AsyncPersistenceHandler
