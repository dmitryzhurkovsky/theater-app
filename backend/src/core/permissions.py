from uuid import UUID

from src.core.deps import AuthenticatedUser, UserServiceDep
from src.core.enums import UserRoleTypeEnum
from src.core.exceptions import AccessError
from src.core.schemas import UserCreate, UserUpdate
from src.models import User


def required_roles(required_roles: list[UserRoleTypeEnum] = []):
    """
    Checks if user has at least one role presented in the required_roles list to access the resource.

    Args:
        required_roles: list[UserRoleTypeEnum] - list of user roles that can access this resource.
        Empty list means that any authorized user can access this resource.
    Raises:
        AccessError: if user doesn't have at least one role from the provided list.
    """

    def role_checker(user: AuthenticatedUser):
        if required_roles and not user.has_at_least_one_role(required_roles):
            raise AccessError from None

    return role_checker


def can_create_user(user: UserCreate, current_user: AuthenticatedUser) -> None:
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
):
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


async def can_delete_user(user_id: UUID, current_user: AuthenticatedUser, user_service: UserServiceDep):
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
