from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from src.models.performance import Performance


class Event(BaseModel, TimestampAbstractModel):
    name: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, nullable=False)
    # TODO: should be implemented Enum choice field
    place: Mapped[str] = mapped_column(default="scena")
    type: Mapped[list["Performance"]] = relationship(
        secondary="user_theatrical_role_relationship",
        back_populates="actor",
        lazy="joined",
    )
    # TODO: should be implemented Enum choice field
    status: Mapped[str] = mapped_column()
