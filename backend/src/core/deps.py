from collections.abc import AsyncGenerator, Generator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError as SessionError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.db import postgres_async_session
from src.core.schemas import ControllerConfig
from src.services import BaseService


async def with_async_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = postgres_async_session()

    try:
        yield session
        await session.commit()
    except SessionError:
        await session.rollback()
    finally:
        await session.close()


def with_controller(
    controller_cls: type[BaseService], config: ControllerConfig = ControllerConfig()
):
    def _controller_loader(session: AsyncSession = Depends(with_async_session)):
        return controller_cls(session, config)

    return _controller_loader
