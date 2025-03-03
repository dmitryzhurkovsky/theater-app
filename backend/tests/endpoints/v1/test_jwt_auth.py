import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from src.models import User
from src.utils import url_for
from tests.factories.schemas import UserRegisterSchemaFactory

fake = Faker()


async def test_register(http_client: AsyncClient):
    user_register_data = UserRegisterSchemaFactory.build()

    response = await http_client.post(
        url=url_for("register"),
        data=user_register_data.model_dump_json(),
        headers={},
    )
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["first_name"] == user_register_data.first_name
    assert body["last_name"] == user_register_data.last_name
    assert body["email"] == user_register_data.email
    assert body["phone_number"] == user_register_data.phone_number
    assert body["user_roles"] == user_register_data.user_roles


@pytest.mark.parametrize("unique_field", ["email", "phone_number"])
async def test_register_unique_error(unique_field: str, user: User, http_client: AsyncClient):
    user_register_data = UserRegisterSchemaFactory.build(**{unique_field: getattr(user, unique_field)})

    response = await http_client.post(
        url=url_for("register"),
        data=user_register_data.model_dump_json(),
        headers={},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


async def test_login_successful(user: User, password: str, http_client: AsyncClient):
    response = await http_client.post(
        url=url_for("login"), data={"username": user.email, "password": password}, headers={}
    )
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in body
    assert "refresh_token" in body


async def test_login_incorrect_data(user: User, password: str, http_client: AsyncClient):
    response = await http_client.post(
        url=url_for("login"), data={"username": user.email, "password": password[::-1]}, headers={}
    )
    body = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert body["detail"] == "Incorrect email or password"


async def test_update_tokens_successful(user: User, password: str, http_client: AsyncClient):
    response = await http_client.post(
        url=url_for("login"), data={"username": user.email, "password": password}, headers={}
    )
    assert response.status_code == status.HTTP_200_OK

    response = await http_client.post(
        url=url_for("update_tokens"), params={"refresh_token": response.json()["refresh_token"]}, headers={}
    )
    body = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in body
    assert "refresh_token" in body


async def test_update_tokens_invalid_token(http_client: AsyncClient):
    response = await http_client.post(
        url=url_for("update_tokens"), params={"refresh_token": fake.pystr(max_chars=30)}, headers={}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"


async def test_update_tokens_user_not_found(mocker, http_client: AsyncClient):
    user_email = fake.email()
    mocker.patch("src.services.security.SecurityService.get_token_payload", return_value={"sub": user_email})

    response = await http_client.post(
        url=url_for("update_tokens"), params={"refresh_token": fake.pystr(max_chars=30)}, headers={}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token. User not found"
