from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.core.enums import NotificationTypeEnum


class NotificationBase(BaseModel):
    user_id: UUID
    event_id: UUID | None = None
    type: NotificationTypeEnum
    text: str | None = None


class NotificationRead(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_read: bool
    created_at: datetime
    updated_at: datetime


class NotificationUpdate(NotificationBase):
    user_id: UUID | None = None
    type: NotificationTypeEnum | None = None
    is_read: bool | None = None
