from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.deps import UserPerformanceRoleServiceDep
from src.core.enums import UserRoleTypeEnum
from src.core.permissions import required_roles
from src.core.schemas import (
    MessageResponseSchema,
    UserPerformanceRoleBase,
    UserPerformanceRoleRead,
    UserPerformanceRoleUpdate,
)

router = APIRouter(prefix="/user-performance-roles", tags=["User performance roles"])


@router.post(
    "/",
    response_model=UserPerformanceRoleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.DIRECTOR, UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]))
    ],
)
async def create_user_performance_role(
    user_performance_role: UserPerformanceRoleBase, user_performance_role_service: UserPerformanceRoleServiceDep
):
    return await user_performance_role_service.create_user_performance_role(user_performance_role)


@router.get(
    "/{user_performance_role_id}", response_model=UserPerformanceRoleRead, dependencies=[Depends(required_roles())]
)
async def get_user_performance_role_by_id(
    user_performance_role_id: UUID, user_performance_role_service: UserPerformanceRoleServiceDep
):
    return await user_performance_role_service.retrieve_user_performance_role(user_performance_role_id)


@router.patch(
    "/{user_performance_role_id}",
    response_model=UserPerformanceRoleRead,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.DIRECTOR, UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]))
    ],
)
async def update_user_performance_role(
    user_performance_role_id: UUID,
    user_performance_role: UserPerformanceRoleUpdate,
    user_performance_role_service: UserPerformanceRoleServiceDep,
):
    return await user_performance_role_service.update_user_performance_role(
        user_performance_role_id, user_performance_role
    )


@router.delete(
    "/{user_performance_role_id}",
    response_model=MessageResponseSchema,
    dependencies=[
        Depends(required_roles([UserRoleTypeEnum.DIRECTOR, UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]))
    ],
)
async def delete_user_performance_role(
    user_performance_role_id: UUID,
    user_performance_role_service: UserPerformanceRoleServiceDep,
):
    return await user_performance_role_service.delete_user_performance_role(user_performance_role_id)
