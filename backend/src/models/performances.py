from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from backend.src.models.theatrical_roles import TheatricalRole


class Performance(BaseModel, TimestampAbstractModel):
    title: Mapped[str] = mapped_column(String(256), unique=True)
    image: Mapped[str]
    description: Mapped[str] = mapped_column(String(1024))
    roles: Mapped[list["TheatricalRole"]] = mapped_column(String())
