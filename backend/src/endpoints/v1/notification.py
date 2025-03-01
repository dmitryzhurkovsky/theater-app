from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.deps import NotificationServiceDep
from src.core.enums import UserRoleTypeEnum
from src.core.permissions import required_roles
from src.core.schemas import (
    MessageResponseSchema,
    NotificationBase,
    NotificationRead,
    NotificationUpdate,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post(
    "/",
    response_model=NotificationRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.DIRECTOR, UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]))
    ],
)
async def create_notification(notification: NotificationBase, notification_service: NotificationServiceDep):
    return await notification_service.create_notification(notification)


@router.get("/{notification_id}", response_model=NotificationRead, dependencies=[Depends(required_roles())])
async def get_notification_by_id(notification_id: UUID, notification_service: NotificationServiceDep):
    return await notification_service.retrieve_notification(notification_id)


@router.patch("/{notification_id}", response_model=NotificationRead, dependencies=[Depends(required_roles())])
async def update_notification(
    notification_id: UUID, notification: NotificationUpdate, notification_service: NotificationServiceDep
):
    return await notification_service.update_notification(notification_id, notification)


@router.delete(
    "/{notification_id}",
    response_model=MessageResponseSchema,
    dependencies=[Depends(required_roles([UserRoleTypeEnum.SUPER_ADMIN]))],
)
async def delete_notification(notification_id: UUID, notification_service: NotificationServiceDep):
    return await notification_service.delete_notification(notification_id)
