from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EventConfirmationBase(BaseModel):
    user_id: UUID
    event_id: UUID


class EventConfirmationRead(EventConfirmationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_approved: bool


class EventConfirmationUpdate(BaseModel):
    is_approved: bool | None = None
