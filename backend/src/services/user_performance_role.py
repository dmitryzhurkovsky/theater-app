from uuid import UUID

from src.core.schemas import UserPerformanceRoleBase, UserPerformanceRoleUpdate
from src.db_managers import UserPerformanceRoleManager
from src.models import UserPerformanceRoleRelationship
from src.services import BaseService


class UserPerformanceRoleService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_performance_role_manager = UserPerformanceRoleManager(self.session)

    async def create_user_performance_role(
        self, user_performance_role: UserPerformanceRoleBase
    ) -> UserPerformanceRoleRelationship:
        return await self.user_performance_role_manager.create(user_performance_role.model_dump())

    async def retrieve_user_performance_role(self, user_performance_role_id: UUID) -> UserPerformanceRoleRelationship:
        return await self.user_performance_role_manager.get_or_404(user_performance_role_id)

    async def update_user_performance_role(
        self, user_performance_role_id: UUID, user_performance_role: UserPerformanceRoleUpdate
    ) -> UserPerformanceRoleRelationship:
        return await self.user_performance_role_manager.update(
            user_performance_role_id, user_performance_role.model_dump(exclude_unset=True)
        )

    async def delete_user_performance_role(self, user_performance_role_id: UUID) -> dict[str, str]:
        obj = await self.user_performance_role_manager.delete(user_performance_role_id)
        return (
            {"message": "User performance role was successfully deleted"}
            if isinstance(obj, UserPerformanceRoleRelationship)
            else obj
        )
