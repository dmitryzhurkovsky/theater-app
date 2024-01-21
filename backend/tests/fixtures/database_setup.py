import pytest_asyncio
from sqlalchemy import text

from src.core.config.settings import settings
from src.core.database.db import postgres_async_engine
from src.core.enums import EnvironmentEnum
from src.models import BaseModel


@pytest_asyncio.fixture(scope="session")
async def database_setup():
    assert settings.ENVIRONMENT == EnvironmentEnum.TEST

    # always drop and create test db tables between tests session
    async with postgres_async_engine.begin() as conn:
        # drop all tables required to make it work with any db condition
        # and it shouldn't depend on the order of the tables or cascade constraints
        await conn.execute(
            text(
                """
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                        IF r.tablename != 'alembic_version' THEN
                            EXECUTE 'DROP TABLE ' || quote_ident(r.tablename) || ' CASCADE';
                        END IF;
                    END LOOP;
                END $$;
                """,
            ),
        )
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
