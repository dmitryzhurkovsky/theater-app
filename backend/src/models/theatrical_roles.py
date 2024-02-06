from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

from src.models import BaseModel

if TYPE_CHECKING:
    from src.models.users import User


class TheatricalRole(BaseModel):

    role_id: Mapped[int] = mapped_column(ForeignKey("theatrical_roles.id"))

    name: Mapped[str] = relationship("Performance",
                                    back_populates="roles",
                                    foreign_keys=[role_id])

    actors: Mapped[list["User"]] = relationship(secondary="user_theatrical_role_relationship",
                                                back_populates="theatrical_role",
                                                lazy="joined")
