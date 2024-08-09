from datetime import date
from typing import List

from sqlalchemy import Date, String
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel, TimestampAbstractModel


class User(BaseModel, TimestampAbstractModel):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True, unique=True)
    photo: Mapped[str]
    birth_date: Mapped[date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    user_roles: Mapped[List[str]] = mapped_column(pg.ARRAY(String), nullable=False)
    viber_link: Mapped[str] = mapped_column(unique=True)
    telegram_link: Mapped[str] = mapped_column(unique=True)
    instagram_link: Mapped[str] = mapped_column(unique=True)
    free_dates: Mapped[List[date]] = mapped_column(pg.ARRAY(Date))
