from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from src.main import app


@pytest_asyncio.fixture(scope="session")
async def http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as http_client:
        http_client.headers.update({"Host": "localhost"})
        yield http_client
