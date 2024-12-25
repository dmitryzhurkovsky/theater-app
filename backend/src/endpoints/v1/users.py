from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.deps import AuthenticatedUser, UserServiceDep
from src.core.permissions import (
    can_create_user,
    can_delete_user,
    can_edit_user,
    required_roles,
)
from src.core.schemas import MessageResponseSchema, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead, dependencies=[Depends(can_create_user)])
async def create_user(user: UserCreate, service: UserServiceDep):
    return await service.create_user(user)


@router.get("/me", response_model=UserRead, summary="Get current user")
async def get_user_me(user: AuthenticatedUser):
    return user


@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(required_roles())])
async def get_user_by_id(user_id: UUID, service: UserServiceDep):
    return await service.retrieve_user(user_id=user_id)


@router.patch("/{user_id}", response_model=UserRead, dependencies=[Depends(can_edit_user)])
async def update_user(user_id: UUID, user: UserUpdate, service: UserServiceDep):
    return await service.update_user(user_id=user_id, user=user)


@router.delete("/{user_id}", response_model=MessageResponseSchema, dependencies=[Depends(can_delete_user)])
async def delete_user(user_id: UUID, service: UserServiceDep):
    return await service.delete_user(user_id=user_id)
