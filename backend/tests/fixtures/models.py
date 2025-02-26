from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from faker import Faker

from src.models import Performance, PerformanceRole, User
from tests.factories.models import (
    PerformanceFactory,
    PerformanceRoleFactory,
    UserFactory,
)


@pytest.fixture
def password() -> Generator[str | None] | str:
    faker = Faker()
    yield faker.password()


@pytest_asyncio.fixture
async def user(password: str) -> AsyncGenerator[User, None] | User:
    user = await UserFactory.create_async(password=password)
    yield user


@pytest_asyncio.fixture
async def performance(user: User) -> AsyncGenerator[Performance, None] | Performance:
    performance = await PerformanceFactory.create_async(director_id=user.id)
    yield performance


@pytest_asyncio.fixture
async def performance_role(performance: Performance) -> AsyncGenerator[PerformanceRole, None] | PerformanceRole:
    performance_role = await PerformanceRoleFactory.create_async(performance_id=performance.id)
    yield performance_role
