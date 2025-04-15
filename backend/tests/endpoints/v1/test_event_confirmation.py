import uuid

import orjson
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from src.core.schemas import EventConfirmationBase, EventConfirmationRead
from src.models import Event, EventConfirmation, User
from src.utils import url_for

fake = Faker()


async def test_create_event_confirmation(admin_client: AsyncClient, event: Event, user: User):
    create_data = {"event_id": str(event.id), "user_id": str(user.id)}
    response = await admin_client.post(
        url_for("create_event_confirmation"), data=orjson.dumps(create_data).decode("utf8")
    )
    body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert EventConfirmationBase(**body) == EventConfirmationBase.model_validate(create_data)


async def test_create_event_confirmation_invalid_event(admin_client: AsyncClient, user: User):
    fake_event_id = uuid.uuid4()
    create_data = {"event_id": str(fake_event_id), "user_id": str(user.id)}
    response = await admin_client.post(
        url_for("create_event_confirmation"), data=orjson.dumps(create_data).decode("utf8")
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == f'Key (event_id)=({fake_event_id}) is not present in table "events".'


async def test_create_event_confirmation_invalid_user(admin_client: AsyncClient, event: Event):
    fake_user_id = uuid.uuid4()
    create_data = {"event_id": str(event.id), "user_id": str(fake_user_id)}
    response = await admin_client.post(
        url_for("create_event_confirmation"), data=orjson.dumps(create_data).decode("utf8")
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == f'Key (user_id)=({fake_user_id}) is not present in table "users".'


async def test_get_event_confirmation_by_id(admin_client: AsyncClient, event_confirmation: EventConfirmation):
    response = await admin_client.get(
        url_for("get_event_confirmation_by_id", event_confirmation_id=str(event_confirmation.id))
    )
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert EventConfirmationRead(**body) == EventConfirmationRead.model_validate(event_confirmation)


async def test_get_event_confirmation_by_id_not_found(admin_client: AsyncClient):
    response = await admin_client.get(url_for("get_event_confirmation_by_id", event_confirmation_id=str(uuid.uuid4())))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_event_confirmation(admin_client: AsyncClient, event_confirmation: EventConfirmation):
    update_data = {"is_approved": True}
    response = await admin_client.patch(
        url_for("update_event_confirmation", event_confirmation_id=str(event_confirmation.id)),
        data=orjson.dumps(update_data).decode("utf8"),
    )
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["id"] == str(event_confirmation.id)
    assert body["is_approved"] is True


async def test_update_event_confirmation_not_found(admin_client: AsyncClient):
    update_data = {"is_approved": True}
    response = await admin_client.patch(
        url_for("update_event_confirmation", event_confirmation_id=str(uuid.uuid4())),
        data=orjson.dumps(update_data).decode("utf8"),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_event_confirmation(super_admin_client: AsyncClient, event_confirmation: EventConfirmation):
    response = await super_admin_client.delete(
        url_for("delete_event_confirmation", event_confirmation_id=str(event_confirmation.id))
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Event confirmation was deleted successfully."


async def test_delete_event_confirmation_not_found(super_admin_client: AsyncClient):
    response = await super_admin_client.delete(
        url_for("delete_event_confirmation", event_confirmation_id=str(uuid.uuid4()))
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
