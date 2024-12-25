from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import JSON, Enum, ForeignKey, String
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums import GenreTypeEnum
from src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from backend.src.models.performance_role import PerformanceRole


class Performance(BaseModel, TimestampAbstractModel):
    __tablename__ = "performances"

    title: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    director_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    image: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    about_author: Mapped[str] = mapped_column(String(1024), nullable=True)
    genre: Mapped[list[GenreTypeEnum]] = mapped_column(
        pg.ARRAY(Enum(*[genre.value for genre in GenreTypeEnum], name="genre_type_enum")),
        nullable=False,
    )
    age: Mapped[int] = mapped_column(default=0, nullable=False)
    annotation: Mapped[str] = mapped_column(String(1024), nullable=True)
    recommendations: Mapped[dict] = mapped_column(type_=JSON, nullable=True)
    need_admin_approve: Mapped[bool] = mapped_column(default=False, nullable=False)
    performance_roles: Mapped[list["PerformanceRole"]] = relationship(back_populates="performance", lazy="selectin")
