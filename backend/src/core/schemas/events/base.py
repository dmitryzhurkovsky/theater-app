from datetime import date, datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    PositiveInt,
    field_validator,
    model_validator,
)

from src.core.enums import EventTypeEnum, StatusTypeEnum
from src.core.exceptions import QueryParamsBuilderException
from src.core.schemas.common import PaginationResponseSchema, QueryParameters
from src.core.schemas.common_validators import validate_day_is_not_previous
from src.core.schemas.event_confirmation import EventConfirmationRead


class EventBase(BaseModel):
    name: str
    date: datetime
    place: str = "scena"
    event_type: EventTypeEnum
    performance_id: UUID | None = None
    duration: PositiveInt = 60


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: StatusTypeEnum
    created_at: datetime
    updated_at: datetime

    confirmations: list[EventConfirmationRead] = []


class EventCreate(EventBase):
    participants: list[UUID] | None = None

    @field_validator("date", mode="after")
    def validate_date(cls, value: datetime) -> datetime:
        return validate_day_is_not_previous(day=value, error_msg="date field cannot contain previous date")


class EventUpdate(EventBase):
    name: str | None = None
    date: datetime | None = None
    place: str | None = None
    event_type: EventTypeEnum | None = None
    status: StatusTypeEnum | None = None
    duration: PositiveInt | None = None

    @field_validator("date", mode="after")
    def validate_date(cls, value: datetime | None) -> datetime | None:
        if value:
            return validate_day_is_not_previous(day=value, error_msg="date field cannot contain previous date")

        return value


class EventQueryParameters(QueryParameters):
    event_type: EventTypeEnum | None = None
    start_date: date | None = None
    end_date: date | None = None
    place: str | None = None
    user_id: UUID | None = None

    @model_validator(mode="after")
    def check_time_period(self) -> "EventQueryParameters":
        if bool(self.start_date) != bool(self.end_date):
            raise QueryParamsBuilderException("start_date and end_date fields should be provided together.")

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise QueryParamsBuilderException("start_date should be before end_date.")
        return self


class EventPaginationResponseSchema(PaginationResponseSchema):
    data: list[EventRead]
