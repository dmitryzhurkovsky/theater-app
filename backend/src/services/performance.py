from uuid import UUID

from src.core.schemas import PerformanceCreate, PerformanceUpdate
from src.db_managers import PerformanceManager
from src.models import Performance
from src.services import BaseService


class PerformanceService(BaseService):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.performance_manager = PerformanceManager(self.session)

    async def create_performance(self, performance: PerformanceCreate) -> Performance:
        return await self.performance_manager.create(performance.model_dump())

    async def retrieve_performance(self, performance_id: UUID) -> Performance:
        return await self.performance_manager.get_or_404(id_=performance_id)

    async def update_performance(self, performance_id: UUID, performance: PerformanceUpdate) -> Performance:
        return await self.performance_manager.update(
            id_=performance_id, update_data=performance.model_dump(exclude_unset=True)
        )

    async def delete_performance(self, performance_id: UUID) -> dict[str, str]:
        obj = await self.performance_manager.delete(obj_id=performance_id)
        return {"message": "Performance was successfully deleted"} if isinstance(obj, Performance) else obj
