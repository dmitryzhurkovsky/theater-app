from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from backend.src.models.events import Event


class EventConfirmation(BaseModel, TimestampAbstractModel):
    __tablename__ = "event_confirmations"
    __table_args__ = (UniqueConstraint("user_id", "event_id", name="idx_user_event"),)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    is_approved: Mapped[bool] = mapped_column(nullable=False, default=False)
    event: Mapped["Event"] = relationship(back_populates="confirmations")
