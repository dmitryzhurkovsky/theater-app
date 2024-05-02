from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base.base import BaseModel


class UserPerformanceRoleRelationship(BaseModel):
    __tablename__ = "user_performance_role_relationship"
    __table_args__ = (UniqueConstraint("user_id", "performance_role_id", name="idx_user_theatrical_role"),)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    performance_role_id: Mapped[UUID] = mapped_column(ForeignKey("performance_roles.id"), nullable=False)
