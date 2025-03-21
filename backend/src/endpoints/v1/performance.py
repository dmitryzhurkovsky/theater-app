from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.deps import PerformanceServiceDep, PerformanceServiceWithConfigDep
from src.core.enums import UserRoleTypeEnum
from src.core.permissions import required_roles
from src.core.schemas import (
    AvailablePerformanceQueryParameters,
    MessageResponseSchema,
    PaginationResponseSchema,
    PerformanceCreate,
    PerformanceQueryParameters,
    PerformanceRead,
    PerformanceUpdate,
)

router = APIRouter(prefix="/performances", tags=["Performances"])


@router.get(
    "/available",
    response_model=list[PerformanceRead],
    dependencies=[Depends(required_roles([UserRoleTypeEnum.SUPER_ADMIN, UserRoleTypeEnum.ADMIN]))],
)
async def get_available_performances(
    service: PerformanceServiceDep, query_parameters: AvailablePerformanceQueryParameters = Depends()
):
    return await service.get_available_performances(day=query_parameters.day)


@router.get("/list", response_model=PaginationResponseSchema, dependencies=[Depends(required_roles())])
async def get_performances(
    service: PerformanceServiceWithConfigDep, query_parameters: PerformanceQueryParameters = Depends()
):
    return await service.get_performances(query_parameters)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PerformanceRead,
    dependencies=[Depends(required_roles([UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]))],
)
async def create_performance(performance: PerformanceCreate, service: PerformanceServiceDep):
    return await service.create_performance(performance)


@router.get("/{performance_id}", response_model=PerformanceRead, dependencies=[Depends(required_roles())])
async def get_performance_by_id(performance_id: UUID, service: PerformanceServiceDep):
    return await service.retrieve_performance(performance_id)


@router.patch(
    "/{performance_id}",
    response_model=PerformanceRead,
    dependencies=[Depends(required_roles([UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]))],
)
async def update_performance(performance_id: UUID, performance: PerformanceUpdate, service: PerformanceServiceDep):
    return await service.update_performance(performance_id=performance_id, performance=performance)


@router.delete(
    "/{performance_id}",
    response_model=MessageResponseSchema,
    dependencies=[Depends(required_roles([UserRoleTypeEnum.SUPER_ADMIN]))],
)
async def delete_performance(performance_id: UUID, service: PerformanceServiceDep):
    return await service.delete_performance(performance_id)
