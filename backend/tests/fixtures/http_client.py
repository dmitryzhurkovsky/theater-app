from collections.abc import AsyncGenerator
from typing import Callable

import pytest_asyncio
from httpx import AsyncClient

from src.core.enums import UserRoleTypeEnum
from src.main import app
from src.utils.security.jwt_token import JWTTokenBuilder
from tests.factories.models import UserFactory


@pytest_asyncio.fixture(scope="session")
async def http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as http_client:
        http_client.headers.update({"Host": "localhost"})
        yield http_client


@pytest_asyncio.fixture
async def authorized_client(
    password: str, http_client: AsyncClient
) -> AsyncGenerator[Callable[[list[UserRoleTypeEnum]], AsyncClient], None]:
    async def _get_client(user_roles: list[UserRoleTypeEnum]) -> AsyncClient:
        user = await UserFactory.create_async(password=password, user_roles=user_roles)
        access_token = JWTTokenBuilder().create_access_token(user=user)

        http_client.headers.update({"Authorization": f"Bearer {access_token}"})
        return http_client

    yield _get_client


@pytest_asyncio.fixture
async def admin_client(authorized_client: AsyncClient) -> AsyncClient:
    return await authorized_client([UserRoleTypeEnum.ADMIN])


@pytest_asyncio.fixture
async def super_admin_client(authorized_client: AsyncClient) -> AsyncClient:
    return await authorized_client([UserRoleTypeEnum.SUPER_ADMIN])
