from typing import Callable
from uuid import UUID

from src.core.deps import AuthenticatedUser, UserServiceDep
from src.core.enums import UserRoleTypeEnum
from src.core.exceptions import AccessError
from src.core.schemas import UserCreate, UserUpdate
from src.models import User


def required_roles(required_roles: list[UserRoleTypeEnum] | None = None) -> Callable[[AuthenticatedUser], None]:
    """
    Checks if user has at least one role presented in the required_roles list to access the resource.

    Args:
        required_roles: list[UserRoleTypeEnum] - list of user roles that can access this resource.
        Empty list means that any authorized user can access this resource.
    Raises:
        AccessError: if user doesn't have at least one role from the provided list.
    """

    def role_checker(user: AuthenticatedUser) -> None:
        if required_roles and not user.has_at_least_one_role(required_roles):
            raise AccessError from None

    return role_checker


def can_create_user(user: UserCreate, current_user: AuthenticatedUser) -> None:
    """
    Checks if user has access to create new user with specific data.

    Args:
        user: UserCreate - data for new user,
        current_user: AuthenticatedUser - user who tries to create new one.
    Raises:
        AccessError: if current_user doesn't have enough permissions to create new user.
        Error cases:
            1. When user tries to create SUPER_ADMIN (it can be done only in the db);
            2. ADMIN user can be created only by SUPER_ADMIN;
            3. DIRECTOR or ACTORS can be created by ADMINS or SUPER_ADMINS.
    """
    if UserRoleTypeEnum.SUPER_ADMIN in user.user_roles:
        raise AccessError from None

    if UserRoleTypeEnum.ADMIN in user.user_roles and not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN):
        raise AccessError from None

    if UserRoleTypeEnum.DIRECTOR in user.user_roles or UserRoleTypeEnum.ACTOR in user.user_roles:
        if not current_user.has_at_least_one_role([UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]):
            raise AccessError from None


async def can_edit_user(
    user_id: UUID,
    user: UserUpdate,
    current_user: AuthenticatedUser,
    user_service: UserServiceDep,
) -> None:
    """
    Checks if user has access to update another user with specific data.

    Args:
        user_id: UUID - id of the user we want to update,
        user: UserUpdate - new data for the user,
        current_user: AuthenticatedUser - user who tries to create new one.
    Raises:
        AccessError: if current_user doesn't have enough permissions to update user with specific data.
        Permissions:
            1. Every User can update itself except user_roles field (only SUPER_ADMIN can do this)
            2. Viewer can be updated only by itself;
            3. DIRECTOR, ACTORS and ADMINS can be updated by SUPER_ADMINS or by themselves.
    """
    target_user: User = await user_service.retrieve_user(user_id=user_id)

    if target_user.has_role(UserRoleTypeEnum.SUPER_ADMIN) and user_id != current_user.id:
        raise AccessError

    if user.user_roles and not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN):
        raise AccessError

    if target_user.has_at_least_one_role([UserRoleTypeEnum.ACTOR, UserRoleTypeEnum.DIRECTOR, UserRoleTypeEnum.ADMIN]):
        if not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN) and user_id != current_user.id:
            raise AccessError

    if target_user.has_role(UserRoleTypeEnum.VIEWER) and user_id != current_user.id:
        raise AccessError


async def can_delete_user(user_id: UUID, current_user: AuthenticatedUser, user_service: UserServiceDep) -> None:
    """
    Checks if user has access to delete user.

    Args:
        user_id: UUID - id of the user we want to delete,
        current_user: AuthenticatedUser - user who tries to delete.
    Raises:
        AccessError: if current_user doesn't have enough permissions to delete user.
        Permissions:
            1. SUPER_ADMIN cannot be deleted (it can be done only in the db);
            2. ADMIN user can be deleted only by SUPER_ADMIN;
            3. DIRECTOR or ACTORS can be deleted by SUPER_ADMINS or by themselves;
            4. VIEWER can be deleted only by itself.
    """
    target_user: User = await user_service.retrieve_user(user_id=user_id)

    if target_user.has_role(UserRoleTypeEnum.SUPER_ADMIN):
        raise AccessError from None

    if target_user.has_role(UserRoleTypeEnum.ADMIN) and not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN):
        raise AccessError from None

    if target_user.has_at_least_one_role([UserRoleTypeEnum.ACTOR, UserRoleTypeEnum.DIRECTOR]):
        if not current_user.has_role(UserRoleTypeEnum.SUPER_ADMIN) and user_id != current_user.id:
            raise AccessError

    if target_user.has_role(UserRoleTypeEnum.VIEWER) and user_id != current_user.id:
        raise AccessError
