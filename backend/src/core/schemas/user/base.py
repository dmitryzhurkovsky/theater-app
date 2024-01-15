from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from src.core.enums import GenderTypeEnum, RoleTypeEnum

if TYPE_CHECKING:
    from src.models.theatrical_roles import TheatricalRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: GenderTypeEnum
    phone_number: str
    birth_date: datetime | None = None
    type: RoleTypeEnum


class UserRead(UserBase):
    id: UUID
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None
    created_at: datetime
    updated_at: datetime

    theatrical_role: list["TheatricalRole"]  # TODO need to replace it with Pydantic model

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None
    theatrical_role: list[int] | None = None


class UserUpdate(UserCreate):
    password: str | None = None
