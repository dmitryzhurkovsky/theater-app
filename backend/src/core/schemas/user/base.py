from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pydantic import BaseModel

from src.core.enums import GenderTypeEnum

if TYPE_CHECKING:
    from src.models.theatrical_roles import TheatricalRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: GenderTypeEnum
    phone_number: str
    birth_date: datetime | None = None
    is_actor: bool = True
    is_admin: bool = False
    is_director: bool = False


class UserRead(UserBase):
    id: UUID
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None
    created_at: datetime
    updated_at: datetime

    # theatrical_role: list[str] #need to implement

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    free_dates: Optional[list[str] | None] = None
    phone_number: Optional[str]
    theatrical_role: Optional[object]  # need to implement
