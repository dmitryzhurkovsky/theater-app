from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from src.core.enums import GenderTypeEnum, UserRoleTypeEnum


class UserBase(BaseModel):
    first_name: str
    last_name: str
    gender: GenderTypeEnum
    phone_number: str
    birth_date: date | None = None
    email: EmailStr
    user_roles: list[UserRoleTypeEnum]


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None
    free_dates: list[date] | None = None
    created_at: datetime
    updated_at: datetime

    # TODO: add theatrical_roles


class UserCreate(UserBase):
    password: str
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None
    free_dates: list[date] | None = None

    @field_validator("free_dates")
    def validate_free_dates(cls, value):
        if value:
            for free_date in value:
                if free_date < date.today():
                    raise ValueError(""" Field "free_dates" cannot contain previos days """)

        return value


class UserUpdate(UserCreate):
    first_name: str | None = None
    last_name: str | None = None
    gender: GenderTypeEnum | None = None
    phone_number: str | None = None
    birth_date: date | None = None
    email: EmailStr | None = None
    user_roles: list[UserRoleTypeEnum] | None = None
    password: str | None = None
