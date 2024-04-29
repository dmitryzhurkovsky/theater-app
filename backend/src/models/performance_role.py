from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel

if TYPE_CHECKING:
    from src.models.users import User


class PerformanceRole(BaseModel):
    __tablename__ = "performance_roles"

    title: Mapped[str] = mapped_column(nullable=False)
    performance_id: Mapped[UUID] = mapped_column(ForeignKey("performances.id"), nullable=False)
