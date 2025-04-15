from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.db import postgres_async_session
from src.models import BaseModel
from tests.factories.models import (
    EventConfirmationFactory,
    EventFactory,
    PerformanceFactory,
    PerformanceRoleFactory,
    UserFactory,
)


@pytest_asyncio.fixture(autouse=True)
async def session(database_setup) -> AsyncGenerator[AsyncSession, None] | AsyncSession:
    async with postgres_async_session() as session:
        yield session

        # delete all data from all tables after test
        for _, table in BaseModel.metadata.tables.items():
            await session.execute(delete(table))
        await session.commit()


@pytest_asyncio.fixture(autouse=True)
def set_async_session_for_factories(session: AsyncSession):
    UserFactory.__async_session__ = session
    PerformanceFactory.__async_session__ = session
    PerformanceRoleFactory.__async_session__ = session
    EventFactory.__async_session__ = session
    EventConfirmationFactory.__async_session__ = session
