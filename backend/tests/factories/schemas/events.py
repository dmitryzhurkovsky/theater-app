import random
from datetime import datetime, timedelta

from faker import Faker
from polyfactory.factories import pydantic_factory

from src.core.enums import EventTypeEnum
from src.core.schemas import EventBase, EventCreate, EventQueryParameters


class EventBaseSchemaFactory(pydantic_factory.ModelFactory[EventBase]):
    __faker__ = Faker()

    @classmethod
    def date(cls) -> datetime:
        return datetime.today() + timedelta(days=random.randint(0, 10))

    @classmethod
    def event_type(cls) -> EventTypeEnum:
        return random.choice(list(EventTypeEnum))


class EventCreateSchemaFactory(EventBaseSchemaFactory):
    __model__ = EventCreate


class EventQueryParametersSchemaFactory(pydantic_factory.ModelFactory[EventQueryParameters]):
    __faker__ = Faker()

    @classmethod
    def event_type(cls) -> EventTypeEnum:
        return random.choice(list(EventTypeEnum))
