from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import EventTypeEnum, StatusTypeEnum


class EventBase(BaseModel):
    name: str
    date: datetime
    place: str = "scena"
    event_type: EventTypeEnum
    performance_id: UUID | None = None
    duration: int = Field(default=60, gt=0)


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: StatusTypeEnum
    created_at: datetime
    updated_at: datetime


class EventUpdate(EventBase):
    name: str | None = None
    date: datetime | None = None
    place: str | None = None
    event_type: EventTypeEnum | None = None
    status: StatusTypeEnum | None = None
    duration: int | None = None
