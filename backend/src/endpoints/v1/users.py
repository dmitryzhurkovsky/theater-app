import logging
from uuid import UUID

import sqlalchemy.exc
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.users import UserService

from src.core.schemas.user.response import (
    UserCreateResponseSchema,
    PaginationResponseSchema,
    UserUpdateResponseSchema,
)
from src.core.schemas import MessageResponseSchema, UserCreate, QueryParameters
from src.core.deps import with_async_session
from src.core.schemas import ControllerConfig

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(
    session: AsyncSession = Depends(with_async_session), config: ControllerConfig = Depends(ControllerConfig)
):
    return UserService(session=session, config=config)


@router.get("/", summary="get users", response_model=PaginationResponseSchema)
async def users(query_params: QueryParameters = Depends(), service: UserService = Depends(get_user_service)):
    return await service.list_users(query_params=query_params)


@router.get("/{id}")
async def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = await service.retrieve_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await service.retrieve_user(user_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponseSchema)
async def create_user(user: UserCreateResponseSchema, service: UserService = Depends(get_user_service)):
    return await service.create_user(user)


@router.patch("/{id}")
async def update_user(
    user_id: UUID, user: UserUpdateResponseSchema, user_service: UserService = Depends(get_user_service)
):
    return await user_service.update_user(user_id, user)


@router.delete("/{id}", response_model=MessageResponseSchema)
async def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    result = await user_service.delete_user(user_id)
    return {"message": "Successfuly deleted user"}
