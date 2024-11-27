from uuid import UUID

from src.core.schemas import PerformanceRoleCreate, PerformanceRoleUpdate
from src.db_managers import PerformanceRoleDatabaseManager
from src.models import PerformanceRole
from src.services.base import BaseService


class PerformanceRoleService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.performance_role_manager = PerformanceRoleDatabaseManager(self.session)

    async def create_performance_role(self, performance_role: PerformanceRoleCreate) -> PerformanceRole:
        return await self.performance_role_manager.create(performance_role.model_dump())

    async def retrieve_performance_role(self, performance_role_id: UUID) -> PerformanceRole:
        return await self.performance_role_manager.get_or_404(performance_role_id)

    async def update_performance_role(
        self, performance_role_id: UUID, performance_role: PerformanceRoleUpdate
    ) -> PerformanceRole:
        return await self.performance_role_manager.update(
            performance_role_id, performance_role.model_dump(exclude_unset=True)
        )

    async def delete_performance_role(self, performance_role_id: UUID) -> dict[str, str]:
        obj = await self.performance_role_manager.delete(performance_role_id)
        return {"message": "Performance role was successfully deleted"} if isinstance(obj, PerformanceRole) else obj
