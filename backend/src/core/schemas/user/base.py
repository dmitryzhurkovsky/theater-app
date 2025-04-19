from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr

from src.core.enums import GenderTypeEnum, UserRoleTypeEnum
from src.core.schemas.user.validators import (
    check_password,
    validate_unavailable_dates,
)


class UserBase(BaseModel):
    first_name: str
    last_name: str
    gender: GenderTypeEnum
    phone_number: str | None = None
    birth_date: date | None = None
    email: EmailStr
    user_roles: list[UserRoleTypeEnum]


class UserAdditionalInfo(BaseModel):
    photo: str | None = None
    viber_link: str | None = None
    telegram_link: str | None = None
    instagram_link: str | None = None


class UserRead(UserBase, UserAdditionalInfo):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    unavailable_dates: list[date] | None = None
    created_at: datetime
    updated_at: datetime

    # TODO: add theatrical_roles


class UserCreate(UserBase, UserAdditionalInfo):
    password: Annotated[str, AfterValidator(check_password)]
    unavailable_dates: Annotated[list[date] | None, AfterValidator(validate_unavailable_dates)] = None


class UserCreateWithOAuth(UserCreate):
    password: str | None = None
    gender: GenderTypeEnum = GenderTypeEnum.NA.value
    user_roles: list[UserRoleTypeEnum] = [UserRoleTypeEnum.VIEWER.value]


class UserUpdate(UserBase, UserAdditionalInfo):
    first_name: str | None = None
    last_name: str | None = None
    gender: GenderTypeEnum | None = None
    phone_number: str | None = None
    birth_date: date | None = None
    email: EmailStr | None = None
    user_roles: list[UserRoleTypeEnum] | None = None
    unavailable_dates: Annotated[list[date] | None, AfterValidator(validate_unavailable_dates)] = None


class UserRegister(UserBase):
    password: Annotated[str, AfterValidator(check_password)]
