from typing import TYPE_CHECKING

from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums import GenreTypeEnum

from src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from src.models.theatrical_roles import TheatricalRole
    from src.models.events import Event


class Performance(BaseModel, TimestampAbstractModel):
    __tablename__ = "performances"

    title: Mapped[str] = mapped_column(String(256), unique=True)
    image: Mapped[str]
    description: Mapped[str] = mapped_column(String(1024))
    author_info: Mapped[str] = mapped_column(String(1024))
    genre: Mapped["GenreTypeEnum"] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(default=0)
    duration_hour: Mapped[int] = mapped_column(default=1, nullable=False)
    duration_min: Mapped[int] = mapped_column(default=0)
    recommendations: Mapped[dict] = mapped_column(type_=JSON)
    need_admin_approve: Mapped[bool] = mapped_column(default=False)

    events: Mapped[list["Event"]] = relationship("Event",
                                                 back_populates="type",
                                                 uselist=True)
