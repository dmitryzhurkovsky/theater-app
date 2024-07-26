import re
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from src.core.enums import GenderTypeEnum, UserRoleTypeEnum


class UserBase(BaseModel):
    first_name: str
    last_name: str
    gender: GenderTypeEnum
    phone_number: str | None = None
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

    @field_validator("free_dates", mode="after")
    def validate_free_dates(cls, value: list[date] | None) -> list[date] | None:
        if value:
            for free_date in value:
                if free_date < date.today():
                    raise ValueError(""" Field "free_dates" cannot contain previous days """)

        return value


class UserCreateWithOAuth(UserCreate):
    password: str | None = None
    gender: GenderTypeEnum = GenderTypeEnum.NA.value
    user_roles: list[UserRoleTypeEnum] = [UserRoleTypeEnum.VIEWER.value]


class UserUpdate(UserCreate):
    first_name: str | None = None
    last_name: str | None = None
    gender: GenderTypeEnum | None = None
    phone_number: str | None = None
    birth_date: date | None = None
    email: EmailStr | None = None
    user_roles: list[UserRoleTypeEnum] | None = None
    password: str | None = None


class UserRegister(UserBase):
    password: str

    @field_validator("password", mode="after")
    def check_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[\W_]", value):
            raise ValueError("Password must contain at least one special character")

        return value
