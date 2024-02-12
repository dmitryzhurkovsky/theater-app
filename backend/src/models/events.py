from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

from src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from src.models.performance import Performance
    from src.models.theatrical_roles import TheatricalRole


class Event(BaseModel, TimestampAbstractModel):
    __tablename__ = "events"

    name: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, nullable=False)
    # TODO: should be implemented Enum choice field
    place: Mapped[str] = mapped_column(default="scena")
    is_approved: Mapped[bool] = mapped_column(default=False)
    performance_id: Mapped[int] = mapped_column(ForeignKey("performances.id"), index=True)
    type: Mapped["Performance"] = relationship("Performance",
                                                back_populates="events",
                                                foreign_keys=[performance_id])
    theatrical_roles: Mapped[list["TheatricalRole"]] = relationship("TheatricalRole",
                                                                    back_populates="name",
                                                                    uselist=True)

