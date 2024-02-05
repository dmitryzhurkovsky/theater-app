from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

from src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from src.models.performance import Performance


class Event(BaseModel, TimestampAbstractModel):
    name: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, nullable=False)
    # TODO: should be implemented Enum choice field
    place: Mapped[str] = mapped_column(default="scena")
    is_approved: Mapped[bool] = mapped_column(unique=False, default=False)
    performance_id: Mapped[int] = mapped_column(ForeignKey("performances.id"))
    type: Mapped["Performance"] = relationship(
        "Performance",
        back_populates="events",
        foreign_keys=[performance_id]
    )

