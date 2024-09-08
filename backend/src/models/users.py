from datetime import date

from sqlalchemy import Date, Enum
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column

from src.core.enums import GenderTypeEnum, UserRoleTypeEnum
from src.models import BaseModel, TimestampAbstractModel


class User(BaseModel, TimestampAbstractModel):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[GenderTypeEnum] = mapped_column(
        Enum(*[gender.value for gender in GenderTypeEnum], name="gender_type_enum"), nullable=False
    )
    phone_number: Mapped[str] = mapped_column(nullable=True, unique=True)
    photo: Mapped[str]
    birth_date: Mapped[date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    user_roles: Mapped[list[UserRoleTypeEnum]] = mapped_column(
        pg.ARRAY(Enum(*[user_role.value for user_role in UserRoleTypeEnum], name="user_role_type_enum")),
        nullable=False,
    )
    viber_link: Mapped[str] = mapped_column(unique=True)
    telegram_link: Mapped[str] = mapped_column(unique=True)
    instagram_link: Mapped[str] = mapped_column(unique=True)
    free_dates: Mapped[list[date]] = mapped_column(pg.ARRAY(Date))

    def has_role(self, role: UserRoleTypeEnum) -> bool:
        return role in self.user_roles

    def has_a_role(self, roles: list[UserRoleTypeEnum]) -> bool:
        for role in roles:
            if role in self.user_roles:
                return True

        return False
