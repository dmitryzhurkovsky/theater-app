import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            declared_attr)

from src.models.base.base import BaseModel


class UserTheatricalRoleRelationship(BaseModel):
    __tablename__ = "user_theatrical_role_relationship"

    __table_args__ = (UniqueConstraint("user_id", "theatrical_role_id", name="idx_user_theatrical_role"),)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    theatrical_role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("theatrical_roles.id"))
