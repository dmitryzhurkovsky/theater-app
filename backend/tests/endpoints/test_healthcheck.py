import pytest
from fastapi import status
from httpx import AsyncClient

from src.utils import url_for


@pytest.mark.asyncio
async def test_healthcheck(http_client: AsyncClient):
    response = await http_client.get(url_for("healthcheck"), headers={})
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["message"] == "success!"
