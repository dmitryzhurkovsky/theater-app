from uuid import UUID

from src.core.schemas import EventBase, EventUpdate
from src.db_managers import EventManager
from src.models import Event
from src.services import BaseService


class EventService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_manager = EventManager(session=self.session)

    async def create_event(self, event: EventBase) -> Event:
        return await self.event_manager.create(event.model_dump())

    async def retrieve_event(self, event_id: UUID) -> Event:
        return await self.event_manager.get_or_404(event_id)

    async def update_event(self, event_id: UUID, event: EventUpdate) -> Event:
        return await self.event_manager.update(event_id, event.model_dump(exclude_unset=True))

    async def delete_event(self, event_id: UUID) -> dict[str, str]:
        obj = await self.event_manager.delete(event_id)
        return {"message": "Event was successfully deleted"} if isinstance(obj, Event) else obj
