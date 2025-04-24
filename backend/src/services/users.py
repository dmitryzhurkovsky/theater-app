from typing import Any, Never, cast
from uuid import UUID

import structlog
from fastapi import HTTPException, status
from pydantic import EmailStr

from src.core.enums import TokenTypeEnum
from src.core.exceptions.auth_exceptions import UserAlreadyExistsException
from src.core.schemas import (
    UserCreate,
    UserCreateWithOAuth,
    UserRegister,
    UserResetPasswordEmailData,
    UserUpdate,
)
from src.db_managers import UserManager
from src.models import User
from src.services import BaseService, SecurityService
from src.utils import build_reset_password_link
from src.utils.security.jwt_token import JWTTokenBuilder
from src.utils.security.password_handler import make_password_hash, verify_password

LOG = structlog.stdlib.get_logger()


class UserService(BaseService):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_manager = UserManager(self.session)
        self.jwt_token_builder = JWTTokenBuilder()

    async def create_user(self, user: UserCreate) -> User:
        hashed_password = make_password_hash(user.password)
        user = user.model_copy(update={"password": hashed_password})

        return await self.user_manager.create(obj_data=user.model_dump())

    async def retrieve_user(self, user_id: UUID) -> User:
        return await self.user_manager.get_or_404(id_=user_id)

    async def update_user(self, user_id: UUID, user: UserUpdate) -> User:
        return await self.user_manager.update(id_=user_id, update_data=user.model_dump(exclude_unset=True))

    async def delete_user(self, user_id: UUID) -> dict[str, str]:
        obj = await self.user_manager.delete(obj_id=user_id)
        return {"message": "User was successfully deleted"} if isinstance(obj, User) else obj

    async def check_if_user_exists(self, email: str) -> Never | None:
        if await self.user_manager.get_by(filters={"email": email}, raise_error=False):
            LOG.error(f"User with {email=} already exists exception")
            raise UserAlreadyExistsException()

    async def register_user(self, user: UserRegister) -> User | dict[str, str]:
        await self.check_if_user_exists(user.email)
        return await self.create_user(user=user)

    async def authenticate_user(self, email: str, password: str) -> User | bool:
        if not (user := await self.user_manager.get_by(filters={"email": email})) or not verify_password(
            password, user.password
        ):
            return False
        return user

    async def login_user(self, email: str, password: str) -> dict[str, str]:
        if not (user := await self.authenticate_user(email, password)):
            LOG.error(f"Authentication error for user {email=}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect email or password")
        return self.jwt_token_builder.get_tokens(user=user)

    async def create_user_with_oauth(self, user_info: dict[str, Any]) -> User | dict[str, str]:
        await self.check_if_user_exists(email=user_info.get("email", ""))

        user = UserCreateWithOAuth(
            first_name=user_info.get("given_name", ""),
            last_name=user_info.get("family_name", ""),
            email=user_info.get("email", ""),
        )
        return await self.create_user(user=user)

    async def get_reset_password_email_data(self, email: str) -> UserResetPasswordEmailData | None:
        if user := await self.user_manager.get_by(filters={"email": email}, raise_error=False):
            LOG.info(f"Reset password for user {user.id}")
            reset_password_token = self.jwt_token_builder.create_password_reset_token(email=email)

            return UserResetPasswordEmailData(
                first_name=cast(str, user.first_name),
                last_name=cast(str, user.last_name),
                user_email=cast(EmailStr, user.email),
                reset_password_link=build_reset_password_link(token=reset_password_token),
            )

        LOG.warning(f"Trying to reset password for email={email}, which is not registered.")
        return None

    async def reset_password(self, token: str, new_password: str) -> None:
        security_service = SecurityService(session=self.session)
        token_payload = security_service.get_token_payload(token=token, token_type=TokenTypeEnum.RESET_PASSWORD)
        user = await self.user_manager.get_by(filters={"email": token_payload.get("sub")})

        await self.user_manager.update(id_=user.id, update_data={"password": make_password_hash(new_password)})
