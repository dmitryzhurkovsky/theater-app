from uuid import UUID

from src.core.schemas import (
    EventBase,
    EventPaginationResponseSchema,
    EventQueryParameters,
    EventUpdate,
)
from src.db_managers import EventManager
from src.models import Event
from src.services import BaseService, EventConfirmationService


class EventService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_manager = EventManager(session=self.session)

    async def get_events(self, query_parameters: EventQueryParameters) -> EventPaginationResponseSchema:
        stmt = self.event_manager.get_by(
            self.event_manager.base_query, filters=query_parameters.model_dump(exclude_none=True, by_alias=True)
        )

        return await super().get_paginated_response(
            model=self.event_manager.model,
            stmt=stmt,
            query_parameters=query_parameters,
            schema=EventPaginationResponseSchema,
        )

    async def create_event(self, event: EventBase) -> Event:
        event = await self.event_manager.create(event.model_dump())

        if event.performance_id:
            event_confirmation_service = EventConfirmationService(session=self.session)
            await event_confirmation_service.notify_performance_participants(
                event_id=event.id, performance_id=event.performance_id
            )

        return event

    async def retrieve_event(self, event_id: UUID) -> Event:
        return await self.event_manager.get_or_404(event_id)

    async def update_event(self, event_id: UUID, event: EventUpdate) -> Event:
        return await self.event_manager.update(event_id, event.model_dump(exclude_unset=True))

    async def delete_event(self, event_id: UUID) -> dict[str, str]:
        obj = await self.event_manager.delete(event_id)
        return {"message": "Event was successfully deleted"} if isinstance(obj, Event) else obj
