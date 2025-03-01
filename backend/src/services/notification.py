from uuid import UUID

from src.core.schemas import NotificationBase, NotificationUpdate
from src.db_managers import NotificationManager
from src.models import Notification
from src.services import BaseService


class NotificationService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification_manager = NotificationManager(session=self.session)

    async def create_notification(self, notification: NotificationBase) -> Notification:
        return await self.notification_manager.create(notification.model_dump())

    async def retrieve_notification(self, notification_id: UUID) -> Notification:
        return await self.notification_manager.get_or_404(notification_id)

    async def update_notification(self, notification_id: UUID, notification: NotificationUpdate) -> Notification:
        return await self.notification_manager.update(notification_id, notification.model_dump(exclude_unset=True))

    async def delete_notification(self, notification_id: UUID) -> Notification:
        obj = await self.notification_manager.delete(notification_id)
        return {"message": "Notification was successfully deleted"} if isinstance(obj, Notification) else obj
