import random
from datetime import datetime, timedelta, timezone

from faker import Faker
from polyfactory.factories import pydantic_factory

from src.core.enums import EventTypeEnum, StatusTypeEnum
from src.core.schemas import EventBase, EventCreate, EventQueryParameters, EventUpdate


class EventBaseSchemaFactory(pydantic_factory.ModelFactory[EventBase]):
    __faker__ = Faker()

    @classmethod
    def date(cls) -> datetime:
        return datetime.now(timezone.utc) + timedelta(days=random.randint(0, 10))

    @classmethod
    def event_type(cls) -> EventTypeEnum:
        return random.choice(list(EventTypeEnum))

    @classmethod
    def status(cls) -> StatusTypeEnum:
        return StatusTypeEnum(cls.__random__.choice(list(StatusTypeEnum)))


class EventCreateSchemaFactory(EventBaseSchemaFactory):
    __model__ = EventCreate


class EventUpdateSchemaFactory(EventCreateSchemaFactory):
    __model__ = EventUpdate

    @classmethod
    def name(cls) -> str:
        return cls.__faker__.word()

    @classmethod
    def place(cls) -> str:
        return cls.__faker__.word()

    @classmethod
    def duration(cls) -> int:
        return cls.__faker__.pyint(min_value=1, max_value=120)


class EventQueryParametersSchemaFactory(pydantic_factory.ModelFactory[EventQueryParameters]):
    __faker__ = Faker()

    @classmethod
    def event_type(cls) -> EventTypeEnum:
        return random.choice(list(EventTypeEnum))
