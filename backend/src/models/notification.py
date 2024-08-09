from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel


class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"), nullable=False)
    is_read: Mapped[bool] = mapped_column(nullable=False, default=False)
    type: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(String(1024))
