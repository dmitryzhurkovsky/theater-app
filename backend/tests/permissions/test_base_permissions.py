import pytest

from src.core.enums import UserRoleTypeEnum
from src.core.exceptions import AccessError
from src.core.permissions import required_roles
from tests.factories.models import UserFactory


@pytest.mark.parametrize(
    "user_roles, require_roles",
    [
        (
            [UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN],
            [UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN],
        ),
        ([UserRoleTypeEnum.ADMIN], [UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]),
        ([UserRoleTypeEnum.ACTOR, UserRoleTypeEnum.VIEWER], [UserRoleTypeEnum.ACTOR, UserRoleTypeEnum.ADMIN]),
        ([UserRoleTypeEnum.VIEWER], []),
    ],
)
async def test_required_roles_successful(user_roles: list[UserRoleTypeEnum], require_roles: list[UserRoleTypeEnum]):
    user = await UserFactory.create_async(user_roles=user_roles)
    role_checker = required_roles(required_roles=require_roles)
    assert role_checker(user=user) is None


@pytest.mark.parametrize(
    "user_roles, require_roles",
    [
        ([UserRoleTypeEnum.VIEWER, UserRoleTypeEnum.ACTOR], [UserRoleTypeEnum.ADMIN]),
        ([UserRoleTypeEnum.ADMIN], [UserRoleTypeEnum.SUPER_ADMIN]),
        ([UserRoleTypeEnum.DIRECTOR], [UserRoleTypeEnum.ACTOR]),
    ],
)
async def test_required_roles_access_error(user_roles: list[UserRoleTypeEnum], require_roles: list[UserRoleTypeEnum]):
    user = await UserFactory.create_async(user_roles=user_roles)
    with pytest.raises(AccessError):
        role_checker = required_roles(required_roles=require_roles)
        role_checker(user=user)
