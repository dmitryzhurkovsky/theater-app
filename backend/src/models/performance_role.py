from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel

if TYPE_CHECKING:
    from src.models.performance import Performance
    from src.models.users import User


class PerformanceRole(BaseModel):
    __table_args__ = (UniqueConstraint("title", "performance_id", name="uq_title_performance_id"),)
    __tablename__ = "performance_roles"

    title: Mapped[str] = mapped_column(nullable=False)
    performance_id: Mapped[UUID] = mapped_column(
        ForeignKey("performances.id", ondelete="CASCADE"), nullable=False, index=True
    )
    performance: Mapped["Performance"] = relationship(back_populates="performance_roles")
    actors: Mapped[list["User"]] = relationship(
        back_populates="theatrical_roles", secondary="user_performance_role_relationship"
    )
