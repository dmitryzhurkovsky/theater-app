from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.db import postgres_async_session
from src.models import BaseModel


@pytest_asyncio.fixture(autouse=True)
async def session(database_setup) -> AsyncGenerator[AsyncSession, None] | AsyncSession:
    async with postgres_async_session() as session:
        yield session

        # delete all data from all tables after test
        for _, table in BaseModel.metadata.tables.items():
            await session.execute(delete(table))
        await session.commit()
