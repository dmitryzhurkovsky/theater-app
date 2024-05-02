from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from src.core.enums import GenderTypeEnum, UserRoleTypeEnum


class UserBase(BaseModel):
    first_name: str
    last_name: str
    gender: GenderTypeEnum
    phone_number: str
    birth_date: date | None = None
    email: str
    user_roles: list[UserRoleTypeEnum]


class UserRead(UserBase):
    id: UUID
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None
    free_dates: list[date] | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None
    free_dates: list[date] | None = None


class UserUpdate(UserCreate):
    password: str | None = None
