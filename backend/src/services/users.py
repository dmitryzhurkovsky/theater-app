from typing import Any, Never
from uuid import UUID

import structlog
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.core.exceptions.auth_exceptions import UserAlreadyExistsException
from src.core.schemas import UserCreate, UserCreateWithOAuth, UserRegister, UserUpdate
from src.db_managers import UserManager
from src.models import User
from src.services.base import BaseService
from src.utils.security.jwt_token import jwt_token
from src.utils.security.password_handler import make_password_hash, verify_password

LOG = structlog.stdlib.get_logger()


class UserService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_manager = UserManager(self.session)

    async def create_user(self, user: UserCreate) -> User | dict[str, str]:
        try:
            return await self.user_manager.create(obj_data=user.model_dump())
        except IntegrityError as ex:
            LOG.error(f"Failed to create user. {ex}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create user.")

    async def retrieve_user(self, user_id: UUID) -> User | dict[str, str]:
        return await self.user_manager.get_or_404(id_=user_id)

    async def update_user(self, user_id: UUID, user: UserUpdate) -> User | dict[str, str]:
        try:
            return await self.user_manager.update(id_=user_id, update_data=user.model_dump(exclude_unset=True))
        except IntegrityError as ex:
            LOG.error(f"Failed to update user. {ex}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to update user.")

    async def delete_user(self, user_id: UUID) -> dict[str, str]:
        obj = await self.user_manager.delete(obj_id=user_id)
        return {"message": "User was successfully deleted"} if isinstance(obj, User) else obj

    async def check_if_user_exists(self, email: str) -> Never | None:
        if await self.user_manager.get_by_email(filters={"email": email}):
            LOG.error(f"User with {email=} already exists exception")
            raise UserAlreadyExistsException()

    async def register_user(self, user: UserRegister) -> User | dict[str, str]:
        await self.check_if_user_exists(user.email)

        hashed_password = make_password_hash(user.password)
        user = user.model_copy(update={"password": hashed_password})
        return await self.create_user(user=user)

    async def authenticate_user(self, email: str, password: str) -> User | bool:
        user = await self.user_manager.get_by_email(filters={"email": email})
        if not user or not verify_password(password, user.password):
            return False
        return user

    async def login_user(self, email: str, password: str) -> dict[str, str]:
        if not (user := await self.authenticate_user(email, password)):
            LOG.error(f"Authentication error for user {email=}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect email or password")

        return jwt_token.get_tokens(user=user)

    async def create_user_with_oauth(self, user_info: dict[str, Any]) -> User | dict[str, str]:
        await self.check_if_user_exists(email=user_info.get("email", ""))

        user = UserCreateWithOAuth(
            first_name=user_info.get("given_name", ""),
            last_name=user_info.get("family_name", ""),
            email=user_info.get("email", ""),
        )
        return await self.create_user(user=user)
