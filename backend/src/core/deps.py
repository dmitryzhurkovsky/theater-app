from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Annotated, Callable, TypeVar

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from sqlalchemy.exc import SQLAlchemyError as SessionError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config.settings import settings
from src.core.database.db import postgres_async_session
from src.core.schemas import ControllerConfig
from src.models import User
from src.services import (
    BaseService,
    EventConfirmationService,
    EventService,
    NotificationService,
    PerformanceRoleService,
    PerformanceService,
    SecurityService,
    UserPerformanceRoleService,
    UserService,
)

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="v1/auth/login")
google_client_secrets: Path = settings.AUTH.GOOGLE_CLIENT_SECRETS_PATH
google_client_scopes: list[str] = settings.AUTH.GOOGLE_CLIENT_SCOPES

T = TypeVar("T", bound=BaseService)


async def with_async_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = postgres_async_session()

    try:
        yield session
        await session.commit()
    except SessionError:
        await session.rollback()
    finally:
        await session.close()


def get_service(service_cls: type[T], with_config: bool = False) -> Callable[[AsyncSession], T]:
    def _service(session: AsyncSession = Depends(with_async_session)) -> T:
        return service_cls(session=session, config=ControllerConfig() if with_config else None)

    return _service


def get_security_service(session: AsyncSession = Depends(with_async_session)) -> SecurityService:
    return SecurityService(session=session)


async def get_auth_user(
    access_token: str = Depends(oauth2_scheme),
    security_service: SecurityService = Depends(get_security_service),
) -> User:
    return await security_service.get_auth_user_by_access_token(access_token=access_token)


def get_google_oauth_flow(request: Request) -> Flow:
    return InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=str(google_client_secrets),
        scopes=google_client_scopes,
        redirect_uri=request.url_for("auth"),
    )


UserServiceDep = Annotated[UserService, Depends(get_service(service_cls=UserService))]
PerformanceServiceDep = Annotated[PerformanceService, Depends(get_service(service_cls=PerformanceService))]
PerformanceRoleServiceDep = Annotated[PerformanceRoleService, Depends(get_service(service_cls=PerformanceRoleService))]
UserPerformanceRoleServiceDep = Annotated[
    UserPerformanceRoleService, Depends(get_service(service_cls=UserPerformanceRoleService))
]
EventServiceDep = Annotated[EventService, Depends(get_service(service_cls=EventService))]
EventConfirmationServiceDep = Annotated[
    EventConfirmationService, Depends(get_service(service_cls=EventConfirmationService))
]
NotificationServiceDep = Annotated[NotificationService, Depends(get_service(service_cls=NotificationService))]

PerformanceServiceWithConfigDep = Annotated[
    PerformanceService, Depends(get_service(service_cls=PerformanceService, with_config=True))
]
EventServiceWithConfigDep = Annotated[EventService, Depends(get_service(service_cls=EventService, with_config=True))]


AuthenticatedUser = Annotated[User, Depends(get_auth_user)]
GoogleOAuthFlow = Annotated[Flow, Depends(get_google_oauth_flow)]
SecurityServiceDep = Annotated[SecurityService, Depends(get_security_service)]
