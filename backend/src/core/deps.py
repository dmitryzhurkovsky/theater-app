from collections.abc import AsyncGenerator
from pathlib import Path

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from sqlalchemy.exc import SQLAlchemyError as SessionError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config.settings import settings
from src.core.database.db import postgres_async_session
from src.core.schemas import ControllerConfig
from src.models import User
from src.services import BaseService, PerformanceService, SecurityService, UserService

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="v1/auth/login")
google_client_secrets: Path = settings.AUTH.GOOGLE_CLIENT_SECRETS_PATH
google_client_scopes: list[str] = settings.AUTH.GOOGLE_CLIENT_SCOPES


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


def get_user_service(session: AsyncSession = Depends(with_async_session)) -> UserService:
    return UserService(session=session)


def get_performance_service(session: AsyncSession = Depends(with_async_session)) -> PerformanceService:
    return PerformanceService(session=session)


def get_security_service(session: AsyncSession = Depends(with_async_session)) -> SecurityService:
    return SecurityService(session=session)


async def get_auth_user(
    access_token: str = Depends(oauth2_scheme),
    security_service: SecurityService = Depends(get_security_service),
) -> User:
    return await security_service.get_auth_user_by_access_token(access_token=access_token)


def get_google_oauth_flow(request: Request) -> Flow:
    return InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=google_client_secrets,
        scopes=google_client_scopes,
        redirect_uri=request.url_for("auth"),
    )
