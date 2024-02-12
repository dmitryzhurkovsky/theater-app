from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

from src.models import BaseModel

if TYPE_CHECKING:
    from src.models.users import User


class TheatricalRole(BaseModel):
    __tablename__ = "theatrical_roles"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), index=True)

    name: Mapped[str] = relationship("Event",
                                    back_populates="theatrical_roles",
                                    foreign_keys=[event_id])

    actors: Mapped[list["User"]] = relationship(secondary="user_theatrical_role_relationship",
                                                back_populates="theatrical_role",
                                                lazy="joined")
