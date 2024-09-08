from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.deps import get_performance_role_service, required_roles
from src.core.enums import UserRoleTypeEnum
from src.core.schemas import (
    MessageResponseSchema,
    PerformanceRoleCreate,
    PerformanceRoleRead,
    PerformanceRoleUpdate,
)
from src.services import PerformanceRoleService

router = APIRouter(prefix="/performance-roles", tags=["Performance roles"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PerformanceRoleRead,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN, UserRoleTypeEnum.DIRECTOR]))
    ],
)
async def create_performance_role(
    performance_role: PerformanceRoleCreate, service: PerformanceRoleService = Depends(get_performance_role_service)
):
    return await service.create_performance_role(performance_role)


@router.get("/{performance_role_id}", response_model=PerformanceRoleRead, dependencies=[Depends(required_roles())])
async def get_performance_role_by_id(
    performance_role_id: UUID, service: PerformanceRoleService = Depends(get_performance_role_service)
):
    return await service.retrieve_performance_role(performance_role_id)


@router.patch(
    "/{performance_role_id}",
    response_model=PerformanceRoleRead,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN, UserRoleTypeEnum.DIRECTOR]))
    ],
)
async def update_performance_role(
    performance_role_id: UUID,
    performance_role: PerformanceRoleUpdate,
    service: PerformanceRoleService = Depends(get_performance_role_service),
):
    return await service.update_performance_role(
        performance_role_id=performance_role_id, performance_role=performance_role
    )


@router.delete(
    "/{performance_role_id}",
    response_model=MessageResponseSchema,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN, UserRoleTypeEnum.DIRECTOR]))
    ],
)
async def delete_performance_role(
    performance_role_id: UUID, service: PerformanceRoleService = Depends(get_performance_role_service)
):
    return await service.delete_performance_role(performance_role_id)
