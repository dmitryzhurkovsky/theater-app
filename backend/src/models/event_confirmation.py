from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base.base import BaseModel


class EventConfirmation(BaseModel):
    __tablename__ = "event_confirmations"
    __table_args__ = (UniqueConstraint("user_id", "event_id", name="idx_user_event"),)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"), nullable=False)
    is_approved: Mapped[bool] = mapped_column(nullable=False, default=False)
