from uuid import UUID

import structlog
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.core.schemas import UserCreate, UserUpdate
from src.db_managers import UserManager
from src.models import User
from src.services.base import BaseService

LOG = structlog.stdlib.get_logger()


class UserService(BaseService):
    def __init__(self, *args, **kwargs) -> None:
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
