from datetime import datetime

from typing import TYPE_CHECKING
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.core.enums import GenderTypeEnum, RoleTypeEnum
from backend.src.models import BaseModel, TimestampAbstractModel

if TYPE_CHECKING:
    from backend.src.models.theatrical_roles import TheatricalRole


class User(BaseModel, TimestampAbstractModel):
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped["GenderTypeEnum"] = mapped_column(nullable=False)
    phone_number: Mapped[str]
    birth_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),  nullable=True)
    photo: Mapped[str]
    type: Mapped["RoleTypeEnum"] = mapped_column(default=RoleTypeEnum.ACTOR.value)
    viber_link: Mapped[str] = mapped_column(nullable=True, unique=True)
    telegram_link: Mapped[str] = mapped_column(nullable=True, unique=True)
    instagram_link: Mapped[str] = mapped_column(nullable=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str]
    theatrical_role: Mapped[list["TheatricalRole"]] = relationship(
        secondary="user_theatrical_role_relationship",
        back_populates="actor"
    )
