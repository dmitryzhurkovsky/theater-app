from collections.abc import AsyncGenerator
from pathlib import Path
from uuid import UUID

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from sqlalchemy.exc import SQLAlchemyError as SessionError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config.settings import settings
from src.core.database.db import postgres_async_session
from src.core.enums import UserRoleTypeEnum
from src.core.exceptions import AccessError
from src.core.schemas import ControllerConfig, UserCreate, UserUpdate
from src.models import User
from src.services import (
    BaseService,
    PerformanceRoleService,
    PerformanceService,
    SecurityService,
    UserService,
)

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


def get_performance_role_service(session: AsyncSession = Depends(with_async_session)) -> PerformanceRoleService:
    return PerformanceRoleService(session=session)


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


def required_roles(required_roles: list[UserRoleTypeEnum] = []):
    def role_checker(user: User = Depends(get_auth_user)):
        if required_roles and not user.has_a_role(required_roles):
            raise AccessError from None

    return role_checker


def can_create_user(user: UserCreate, current_user: User = Depends(get_auth_user)) -> None:
    if UserRoleTypeEnum.SUPER_ADMIN in user.user_roles:
        raise AccessError from None

    if UserRoleTypeEnum.ADMIN in user.user_roles and not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN):
        raise AccessError from None

    if UserRoleTypeEnum.DIRECTOR in user.user_roles or UserRoleTypeEnum.ACTOR in user.user_roles:
        if not current_user.has_a_role([UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]):
            raise AccessError from None


async def can_edit_user(
    user_id: UUID,
    user: UserUpdate,
    current_user: User = Depends(get_auth_user),
    user_service: UserService = Depends(get_user_service),
):
    target_user: User = await user_service.retrieve_user(user_id=user_id)

    if target_user.has_role(UserRoleTypeEnum.SUPER_ADMIN) and user_id != current_user.id:
        raise AccessError

    if user.user_roles and not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN):
        raise AccessError

    if target_user.has_a_role([UserRoleTypeEnum.ACTOR, UserRoleTypeEnum.DIRECTOR, UserRoleTypeEnum.ADMIN]):
        if not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN) and user_id != current_user.id:
            raise AccessError

    if target_user.has_role(UserRoleTypeEnum.VIEWER) and user_id != current_user.id:
        raise AccessError


async def can_delete_user(
    user_id: UUID, current_user: User = Depends(get_auth_user), user_service: UserService = Depends(get_user_service)
):
    target_user: User = await user_service.retrieve_user(user_id=user_id)

    if target_user.has_role(UserRoleTypeEnum.SUPER_ADMIN):
        raise AccessError from None

    if target_user.has_role(UserRoleTypeEnum.ADMIN) and not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN):
        raise AccessError from None

    if target_user.has_a_role([UserRoleTypeEnum.ACTOR, UserRoleTypeEnum.DIRECTOR]):
        if not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN) and user_id != current_user.id:
            raise AccessError

    if target_user.has_role(UserRoleTypeEnum.VIEWER) and user_id != current_user.id:
        raise AccessError
