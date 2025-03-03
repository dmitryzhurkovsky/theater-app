from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.enums import EventTypeEnum, StatusTypeEnum
from src.models import BaseModel, TimestampAbstractModel


class Event(BaseModel, TimestampAbstractModel):
    __tablename__ = "events"

    name: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, nullable=False)
    place: Mapped[str] = mapped_column(nullable=False, default="scena")
    event_type: Mapped[EventTypeEnum] = mapped_column(
        Enum(*[event_type.value for event_type in EventTypeEnum], name="event_type_enum"), nullable=False
    )
    status: Mapped[StatusTypeEnum] = mapped_column(
        Enum(*[status.value for status in StatusTypeEnum], name="status_type_enum"),
        nullable=False,
    )
    performance_id: Mapped[UUID] = mapped_column(
        ForeignKey("performances.id", ondelete="CASCADE"), nullable=True, index=True
    )
    duration: Mapped[int] = mapped_column(nullable=False, default=60)
