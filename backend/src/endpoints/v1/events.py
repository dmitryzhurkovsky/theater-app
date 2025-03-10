from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.deps import EventServiceDep, EventServiceWithConfigDep
from src.core.enums import UserRoleTypeEnum
from src.core.permissions import required_roles
from src.core.schemas import (
    EventBase,
    EventPaginationResponseSchema,
    EventQueryParameters,
    EventRead,
    EventUpdate,
    MessageResponseSchema,
)

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/list", response_model=EventPaginationResponseSchema, dependencies=[Depends(required_roles())])
async def get_events(event_service: EventServiceWithConfigDep, query_parameters: EventQueryParameters = Depends()):
    return await event_service.get_events(query_parameters=query_parameters)


@router.post(
    "/",
    response_model=EventRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.DIRECTOR, UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]))
    ],
)
async def create_event(event: EventBase, event_service: EventServiceDep):
    return await event_service.create_event(event)


@router.get("/{event_id}", response_model=EventRead, dependencies=[Depends(required_roles())])
async def get_event_by_id(event_id: UUID, event_service: EventServiceDep):
    return await event_service.retrieve_event(event_id)


@router.patch(
    "/{event_id}",
    response_model=EventRead,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.DIRECTOR, UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]))
    ],
)
async def update_event(event_id: UUID, event: EventUpdate, event_service: EventServiceDep):
    return await event_service.update_event(event_id, event)


@router.delete(
    "/{event_id}",
    response_model=MessageResponseSchema,
    dependencies=[Depends(required_roles([UserRoleTypeEnum.SUPER_ADMIN]))],
)
async def delete_event(event_id: UUID, event_service: EventServiceDep):
    return await event_service.delete_event(event_id)
