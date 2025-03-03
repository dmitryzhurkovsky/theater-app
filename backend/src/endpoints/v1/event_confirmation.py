from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.deps import EventConfirmationServiceDep
from src.core.enums import UserRoleTypeEnum
from src.core.permissions import required_roles
from src.core.schemas import (
    EventConfirmationBase,
    EventConfirmationRead,
    EventConfirmationUpdate,
    MessageResponseSchema,
)

router = APIRouter(prefix="/event-confirmations", tags=["Event confirmations"])


@router.post(
    "/",
    response_model=EventConfirmationRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.DIRECTOR, UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]))
    ],
)
async def create_event_confirmation(
    event_confirmation: EventConfirmationBase, event_confirmation_service: EventConfirmationServiceDep
):
    return await event_confirmation_service.create_event_confirmation(event_confirmation)


@router.get("/{event_confirmation_id}", response_model=EventConfirmationRead, dependencies=[Depends(required_roles())])
async def get_event_confirmation_by_id(
    event_confirmation_id: UUID, event_confirmation_service: EventConfirmationServiceDep
):
    return await event_confirmation_service.retrieve_event_confirmation(event_confirmation_id)


@router.patch(
    "/{event_confirmation_id}", response_model=EventConfirmationRead, dependencies=[Depends(required_roles())]
)
async def update_event_confirmation(
    event_confirmation_id: UUID,
    event_confirmation: EventConfirmationUpdate,
    event_confirmation_service: EventConfirmationServiceDep,
):
    return await event_confirmation_service.update_event_confirmation(event_confirmation_id, event_confirmation)


@router.delete(
    "/{event_confirmation_id}",
    response_model=MessageResponseSchema,
    dependencies=[Depends(required_roles([UserRoleTypeEnum.SUPER_ADMIN]))],
)
async def delete_event_confirmation(
    event_confirmation_id: UUID, event_confirmation_service: EventConfirmationServiceDep
):
    return await event_confirmation_service.delete_event_confirmation(event_confirmation_id)
