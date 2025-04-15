import uuid
from datetime import datetime, time, timedelta, timezone
from typing import Any

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enums import EventTypeEnum
from src.core.schemas import EventCreate, EventRead, EventUpdate
from src.db_managers import EventManager
from src.models import Event, Performance, User
from src.utils import url_for
from tests.factories.models import EventConfirmationFactory, EventFactory, UserFactory
from tests.factories.schemas import EventCreateSchemaFactory, EventUpdateSchemaFactory

fake = Faker()


async def test_list_events_no_results(admin_client: AsyncClient):
    response = await admin_client.get(url_for("get_events"), params={"place": fake.word()})
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["data"] == []


async def test_list_events_by_event_type(admin_client: AsyncClient):
    await EventFactory.create_batch_async(2, event_type=EventTypeEnum.PERFORMANCE)
    await EventFactory.create_batch_async(2, event_type=EventTypeEnum.REHEARSAL)

    response = await admin_client.get(url_for("get_events"), params={"event_type": EventTypeEnum.PERFORMANCE.value})
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(body["data"]) == 2
    for event_res in body["data"]:
        assert event_res["event_type"] == EventTypeEnum.PERFORMANCE


async def test_list_events_by_multiple_fields(admin_client: AsyncClient):
    place = fake.word()
    await EventFactory.create_batch_async(2, event_type=EventTypeEnum.PERFORMANCE, place=place)
    await EventFactory.create_batch_async(2, event_type=EventTypeEnum.REHEARSAL, place=place)

    response = await admin_client.get(
        url_for("get_events"), params={"event_type": EventTypeEnum.PERFORMANCE.value, "place": place}
    )
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(body["data"]) == 2
    for event_res in body["data"]:
        assert event_res["event_type"] == EventTypeEnum.PERFORMANCE
        assert event_res["place"] == place


async def test_list_events_by_time_range(admin_client: AsyncClient):
    for i in range(6):
        event_time = datetime.now() + timedelta(days=i)
        await EventFactory.create_async(date=event_time)

    days_number = fake.pyint(min_value=0, max_value=5)
    start_date = datetime.today()
    end_date = start_date + timedelta(days=days_number)
    response = await admin_client.get(
        url_for("get_events"),
        params={"start_date": start_date.strftime("%Y-%m-%d"), "end_date": end_date.strftime("%Y-%m-%d")},
    )
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(body["data"]) == days_number + 1

    for event_res in body["data"]:
        event_res_date = datetime.fromisoformat(event_res["date"])
        assert event_res_date >= datetime.combine(start_date, time.min).replace(tzinfo=timezone.utc)
        assert event_res_date <= datetime.combine(end_date, time.max).replace(tzinfo=timezone.utc)


async def test_list_user_events(admin_client: AsyncClient):
    num_of_objects = 2
    users = await UserFactory.create_batch_async(num_of_objects)
    events = await EventFactory.create_batch_async(num_of_objects)

    for i in range(num_of_objects):
        await EventConfirmationFactory.create_async(event_id=events[i].id, user_id=users[i].id)

    response = await admin_client.get(url_for("get_events"), params={"user_id": str(users[0].id)})
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(body["data"]) == 1

    confirmations = body["data"][0]["confirmations"]
    assert len(confirmations) == 1
    assert confirmations[0]["event_id"] == str(events[0].id)
    assert confirmations[0]["user_id"] == str(users[0].id)


async def test_create_event_without_participants(admin_client: AsyncClient, performance: Performance):
    create_data = EventCreateSchemaFactory.build(performance_id=performance.id, participants=None)

    response = await admin_client.post(url_for("create_event"), data=create_data.model_dump_json())
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()

    assert body["confirmations"] == []
    assert EventCreate(**body) == create_data


async def test_create_event_with_participants(admin_client: AsyncClient, user: User):
    create_data = EventCreateSchemaFactory.build(performance_id=None, participants=[user.id])

    response = await admin_client.post(url_for("create_event"), data=create_data.model_dump_json())
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()

    assert EventCreate(**body, participants=[user.id]) == create_data
    assert len(body["confirmations"]) == 1
    assert body["confirmations"][0]["user_id"] == str(user.id)
    assert body["confirmations"][0]["event_id"] == body["id"]


async def test_create_event_incorrect_participants(admin_client: AsyncClient, session: AsyncSession):
    fake_user_id = uuid.uuid4()
    create_data = EventCreateSchemaFactory.build(performance_id=None, participants=[fake_user_id])

    response = await admin_client.post(url_for("create_event"), data=create_data.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == f'Key (user_id)=({fake_user_id}) is not present in table "users".'

    # checking that event is not saved in the db
    event_manager = EventManager(session=session)
    result = await event_manager._list(filters={"name": create_data.name})

    assert result == []


async def test_create_event_incorrect_performance(admin_client: AsyncClient):
    fake_performance_id = uuid.uuid4()
    create_data = EventCreateSchemaFactory.build(performance_id=fake_performance_id, participants=None)

    response = await admin_client.post(url_for("create_event"), data=create_data.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT
    assert (
        response.json()["detail"]
        == f'Key (performance_id)=({fake_performance_id}) is not present in table "performances".'
    )


async def test_get_event_by_id(event: Event, admin_client: AsyncClient):
    response = await admin_client.get(url_for("get_event_by_id", event_id=str(event.id)))
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert EventRead(**body) == EventRead.model_validate(event)


async def test_get_event_by_id_not_found(admin_client: AsyncClient):
    response = await admin_client.get(url_for("get_event_by_id", event_id=str(uuid.uuid4())))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_event_successful(admin_client: AsyncClient, event: Event, performance: Performance):
    update_data = EventUpdateSchemaFactory.build(performance_id=performance.id)

    response = await admin_client.patch(
        url_for("update_event", event_id=str(event.id)), data=update_data.model_dump_json()
    )
    assert response.status_code == status.HTTP_200_OK
    body = response.json()

    assert EventUpdate(**body) == update_data


@pytest.mark.parametrize(
    "field_name, field_value",
    [
        ("name", None),
        ("date", None),
        ("place", None),
        ("event_type", None),
        ("status", None),
        ("duration", None),
        ("performance_id", uuid.uuid4()),
    ],
)
async def test_update_event_conflict(field_name: str, field_value: Any, admin_client: AsyncClient, event: Event):
    update_data = EventUpdateSchemaFactory.build(**{field_name: field_value})

    response = await admin_client.patch(
        url_for("update_event", event_id=str(event.id)), data=update_data.model_dump_json()
    )
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_update_event_not_found(admin_client: AsyncClient):
    update_data = EventUpdateSchemaFactory.build()

    response = await admin_client.patch(
        url_for("update_event", event_id=str(uuid.uuid4())), data=update_data.model_dump_json()
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_event(event: Event, super_admin_client: AsyncClient):
    response = await super_admin_client.delete(url_for("delete_event", event_id=str(event.id)))

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Event was successfully deleted"


async def test_delete_event_not_found(super_admin_client: AsyncClient):
    response = await super_admin_client.delete(url_for("delete_event", event_id=str(uuid.uuid4())))
    assert response.status_code == status.HTTP_404_NOT_FOUND
