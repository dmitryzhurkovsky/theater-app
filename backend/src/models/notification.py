from uuid import UUID

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.enums import NotificationTypeEnum
from src.models import BaseModel


class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    is_read: Mapped[bool] = mapped_column(nullable=False, default=False)
    type: Mapped[NotificationTypeEnum] = mapped_column(
        Enum(*[notification_type.value for notification_type in NotificationTypeEnum], name="notification_type_enum"),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(String(1024))
