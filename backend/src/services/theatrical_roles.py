from src.core.schemas import (
    PaginationResponseSchema,
    QueryParameters,
    TheatricalRoleCreate,
    TheatricalRoleUpdate,
)
from src.db_managers import TheatricalRoleDatabaseManager
from src.models import TheatricalRole
from src.services.base import BaseService


class TheatricalRoleService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theatrical_role_manager = TheatricalRoleDatabaseManager(self.session)

    async def list_theatrical_roles(self, query_params: QueryParameters) -> PaginationResponseSchema:
        return await self.get_paginated_response(
            self.theatrical_role_manager.model,
            self.theatrical_role_manager.base_query,
            query_params,
        )

    async def create_theatrical_role(self, theatrical_role: TheatricalRoleCreate) -> TheatricalRole:
        return await self.theatrical_role_manager.create(theatrical_role.model_dump())

    async def retrieve_theatrical_role(self, thr_id: int) -> TheatricalRole:
        return await self.theatrical_role_manager.get_or_404(thr_id)

    async def update_theatrical_role(self, thr_id: int, theatrical_role: TheatricalRoleUpdate) -> TheatricalRole:
        return await self.theatrical_role_manager.update(thr_id, theatrical_role.model_dump())

    async def delete_theatrical_role(self, thr_id: int) -> TheatricalRole:
        return await self.theatrical_role_manager.delete(thr_id)
