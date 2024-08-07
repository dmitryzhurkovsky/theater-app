from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import JSON, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums import GenreTypeEnum
from src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from backend.src.models.performance_role import PerformanceRole
    from src.models.events import Event


class Performance(BaseModel, TimestampAbstractModel):
    __tablename__ = "performances"

    title: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    director_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    image: Mapped[str]
    description: Mapped[str] = mapped_column(String(1024))
    about_author: Mapped[str] = mapped_column(String(1024))
    genre: Mapped[GenreTypeEnum] = mapped_column(
        Enum(*[genre.value for genre in GenreTypeEnum], name="genre_type_enum"),
        nullable=False,
    )
    age: Mapped[int] = mapped_column(default=0, nullable=False)
    annotation: Mapped[str] = mapped_column(String(1024))
    recommendations: Mapped[dict] = mapped_column(type_=JSON)
    need_admin_approve: Mapped[bool] = mapped_column(default=False)
    performance_roles: Mapped[List["PerformanceRole"]] = relationship(back_populates="performance", lazy="selectin")
