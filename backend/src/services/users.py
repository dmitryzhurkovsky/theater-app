from datetime import datetime

from src.core.schemas import PaginationResponseSchema, QueryParameters
from src.db_managers.users import UserManager
from src.services.base import BaseService
from uuid import UUID

from src.core.schemas.user.response import UserCreateResponseSchema
from src.models.users import User
from src.core.schemas.user.response import UserUpdateResponseSchema


class UserService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_manager = UserManager(self.session)

    async def list_users(self, query_params: QueryParameters) -> PaginationResponseSchema:
        return await self.get_paginated_response(
            self.user_manager.model,
            self.user_manager.base_query,
            query_params,
        )

    async def create_user(self, user: UserCreateResponseSchema) -> User:
        return await self.user_manager.create(obj_data=user.data.model_dump())

    async def retrieve_user(self, user_uuid: UUID) -> User:
        return await self.user_manager.get_or_404(user_uuid)

    async def update_user(self, user_uuid: UUID, user: UserUpdateResponseSchema) -> User:
        user_to_update = user.data
        free_dates = user_to_update.free_dates
        if "string" not in free_dates:
            """parse into date format"""
            date_objects = [datetime.strptime(date_string, "%Y-%m-%d") for date_string in free_dates]
            user_to_update.free_dates = date_objects

        return await self.user_manager.update(user_uuid, user_to_update.model_dump())

    async def delete_user(self, user_uuid: UUID) -> User:
        return await self.user_manager.delete(user_uuid)
