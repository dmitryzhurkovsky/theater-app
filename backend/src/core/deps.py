from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError as SessionError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.db import postgres_async_session
from src.core.enums.jwt_token import TokenEnum
from src.core.schemas import ControllerConfig
from src.services import BaseService, SecurityService, UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"v1/auth/login")


async def with_async_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = postgres_async_session()

    try:
        yield session
        await session.commit()
    except SessionError:
        await session.rollback()
    finally:
        await session.close()


def with_service(service_cls: type[BaseService], config: ControllerConfig = ControllerConfig()):
    def _service_loader(session: AsyncSession = Depends(with_async_session)):
        return service_cls(session, config)

    return _service_loader


def get_user_service(session: AsyncSession = Depends(with_async_session)):
    return UserService(session=session)


def get_security_service(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(with_async_session)):
    return SecurityService(user_token=token, session=session)


async def get_user_from_access_token(security_service: SecurityService = Depends(get_security_service)):
    return await security_service.get_auth_user(TokenEnum.ACCESS.value)
