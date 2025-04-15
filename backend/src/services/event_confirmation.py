from uuid import UUID

from src.core.schemas import EventConfirmationBase, EventConfirmationUpdate
from src.db_managers import EventConfirmationManager
from src.models import EventConfirmation
from src.services import BaseService


class EventConfirmationService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_confirmation_manager = EventConfirmationManager(session=self.session)

    async def create_event_confirmation(self, event_confirmation: EventConfirmationBase) -> EventConfirmation:
        return await self.event_confirmation_manager.create(event_confirmation.model_dump())

    async def retrieve_event_confirmation(self, event_confirmation_id: UUID) -> EventConfirmation:
        return await self.event_confirmation_manager.get_or_404(event_confirmation_id)

    async def update_event_confirmation(
        self, event_confirmation_id: UUID, event_confirmation: EventConfirmationUpdate
    ) -> EventConfirmation:
        return await self.event_confirmation_manager.update(
            event_confirmation_id, event_confirmation.model_dump(exclude_unset=True)
        )

    async def delete_event_confirmation(self, event_confirmation_id: UUID) -> dict[str, str]:
        obj = await self.event_confirmation_manager.delete(event_confirmation_id)
        return (
            {"message": "Event confirmation was deleted successfully."} if isinstance(obj, EventConfirmation) else obj
        )

    async def notify_event_participants(self, event_id: UUID, participants: list[UUID]) -> None:
        confirmations_info = [{"event_id": event_id, "user_id": user_id} for user_id in participants]
        await self.event_confirmation_manager.insert_many(data=confirmations_info)
