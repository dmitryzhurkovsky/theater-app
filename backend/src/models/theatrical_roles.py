from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship
from src.models import BaseModel

if TYPE_CHECKING:
    from src.models.users import User


class TheatricalRole(BaseModel):
    name: Mapped[str]
    actors: Mapped[list["User"]] = relationship(
        secondary="user_theatrical_role_relationship", back_populates="theatrical_role"
    )
