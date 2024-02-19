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
from src.core.schemas import MessageResponseSchema
from src.core.deps import with_async_session
from src.core.schemas import ControllerConfig
from src.core.schemas.common.query import QueryParameters
from src.core.schemas.common.pagination import Pagination

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(session: AsyncSession = Depends(with_async_session)):
    return UserService(session=session)


def user_service_pagination(
    session: AsyncSession = Depends(with_async_session), config: ControllerConfig = Depends(ControllerConfig)
):
    return UserService(session=session, config=config)


@router.post("", summary="get users", response_model=PaginationResponseSchema)
async def users(user_service: UserService = Depends(user_service_pagination)):
    pagination = Pagination(page=1, per_page=10)
    params = QueryParameters(pagination=pagination)
    users_res_test = await user_service.list_users(params)

    return users_res_test


@router.get("/{id}")
async def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = await service.retrieve_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": user}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponseSchema | MessageResponseSchema)
async def create_user(user: UserCreateResponseSchema, service: UserService = Depends(get_user_service)):
    try:
        user_obj = await service.create_user(user)
        return {"data": user_obj}
    except sqlalchemy.exc.IntegrityError as e:
        logging.error(e)
        return {"message": "Failed to create user"}


@router.patch("/{id}")
async def update_user(
    user_id: UUID, user: UserUpdateResponseSchema, user_service: UserService = Depends(get_user_service)
):
    result = await user_service.update_user(user_id, user)

    return {"data": user}


@router.delete("/{id}", response_model=MessageResponseSchema)
async def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    result = await user_service.delete_user(user_id)
    return {"message": "Successfuly deleted user"}
