from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from src.core.schemas.user_base.base import UserBase


class UserRead(UserBase):
    id: UUID
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None
    created_at: datetime
    updated_at: datetime
    theatrical_role: list[UUID]

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    free_dates: list[str] | None = None
    phone_number: str | None = None
    theatrical_role: List[UUID] = None
