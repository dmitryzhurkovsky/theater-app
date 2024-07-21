from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.core.deps import get_auth_user, get_user_service
from src.core.schemas import MessageResponseSchema, UserCreate, UserRead, UserUpdate
from src.services import SecurityService, UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(user)


@router.get("/me", response_model=UserRead, summary="Get current user")
async def get_user_me(user: SecurityService = Depends(get_auth_user)):
    return user


@router.get("/{id}", response_model=UserRead)
async def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):
    return await service.retrieve_user(user_id=user_id)


@router.patch("/{id}", response_model=UserRead)
async def update_user(user_id: UUID, user: UserUpdate, service: UserService = Depends(get_user_service)):
    return await service.update_user(user_id=user_id, user=user)


@router.delete("/{id}", response_model=MessageResponseSchema)
async def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    return await service.delete_user(user_id=user_id)
