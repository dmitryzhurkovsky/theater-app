from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums import GenderTypeEnum
from src.models import BaseModel, TimestampAbstractModel

from sqlalchemy.dialects.postgresql import ARRAY

if TYPE_CHECKING:
    from src.models.theatrical_roles import TheatricalRole


class User(BaseModel, TimestampAbstractModel):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped["GenderTypeEnum"] = mapped_column(nullable=False)
    phone_number: Mapped[str]
    birth_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    photo: Mapped[str]
    is_actor: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_director: Mapped[bool] = mapped_column(default=False)
    viber_link: Mapped[str] = mapped_column(nullable=True, unique=True)
    telegram_link: Mapped[str] = mapped_column(nullable=True, unique=True)
    instagram_link: Mapped[str] = mapped_column(nullable=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str]
    free_dates: Mapped[list[datetime]] = mapped_column(ARRAY(DateTime(timezone=True)), nullable=True, default=None)

    theatrical_role: Mapped[list["TheatricalRole"]] = relationship(
        secondary="user_theatrical_role_relationship", back_populates="actors"
    )
