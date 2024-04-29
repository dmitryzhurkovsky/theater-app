from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.enums import EventTypeEnum, StatusTypeEnum
from src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from src.models.performance import Performance


class Event(BaseModel, TimestampAbstractModel):
    __tablename__ = "events"

    name: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, nullable=False)
    place: Mapped[str] = mapped_column(nullable=False, default="scena")
    event_type: Mapped[EventTypeEnum] = mapped_column(nullable=False)
    status: Mapped[StatusTypeEnum] = mapped_column(nullable=False)
    performance_id: Mapped[UUID] = mapped_column(ForeignKey("performances.id"), nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False, default=60)
