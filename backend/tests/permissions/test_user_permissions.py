import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enums import UserRoleTypeEnum
from src.core.exceptions import AccessError
from src.core.permissions import can_create_user, can_delete_user, can_edit_user
from src.core.schemas import UserUpdate
from src.models import User
from src.services import UserService
from tests.factories.models import UserFactory
from tests.factories.schemas import UserCreateSchemaFactory

faker = Faker()


async def create_test_users(
    current_user_roles: list[UserRoleTypeEnum], target_user_roles: list[UserRoleTypeEnum] = None
) -> tuple[User]:
    current_user = await UserFactory.create_async(user_roles=current_user_roles)
    target_user = None
    if target_user_roles:
        target_user = await UserFactory.create_async(user_roles=target_user_roles)
    return current_user, target_user


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_create_roles, current_user_roles",
    [
        ([UserRoleTypeEnum.ADMIN], [UserRoleTypeEnum.SUPER_ADMIN]),
        ([UserRoleTypeEnum.DIRECTOR], [UserRoleTypeEnum.ADMIN]),
        ([UserRoleTypeEnum.ACTOR], [UserRoleTypeEnum.ADMIN]),
        ([UserRoleTypeEnum.DIRECTOR], [UserRoleTypeEnum.ADMIN]),
    ],
)
async def test_can_create_user_successful(
    user_create_roles: list[UserRoleTypeEnum], current_user_roles: list[UserRoleTypeEnum]
):
    current_user = await UserFactory.create_async(user_roles=current_user_roles)
    user_create_data = UserCreateSchemaFactory.build(user_roles=user_create_roles)

    assert can_create_user(user=user_create_data, current_user=current_user) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_create_roles, current_user_roles",
    [
        ([UserRoleTypeEnum.SUPER_ADMIN], [UserRoleTypeEnum.ADMIN, UserRoleTypeEnum.SUPER_ADMIN]),
        ([UserRoleTypeEnum.ADMIN], [UserRoleTypeEnum.ACTOR, UserRoleTypeEnum.ADMIN]),
        ([UserRoleTypeEnum.ACTOR], [UserRoleTypeEnum.DIRECTOR]),
        ([UserRoleTypeEnum.DIRECTOR], [UserRoleTypeEnum.ACTOR]),
    ],
)
async def test_can_create_user_access_error(
    user_create_roles: list[UserRoleTypeEnum], current_user_roles: list[UserRoleTypeEnum]
):
    current_user = await UserFactory.create_async(user_roles=current_user_roles)
    user_create_data = UserCreateSchemaFactory.build(user_roles=user_create_roles)

    with pytest.raises(AccessError):
        can_create_user(user=user_create_data, current_user=current_user)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_to_delete_roles, current_user_roles",
    [
        ([UserRoleTypeEnum.ADMIN], [UserRoleTypeEnum.SUPER_ADMIN]),
        ([UserRoleTypeEnum.ACTOR], [UserRoleTypeEnum.SUPER_ADMIN]),
        ([UserRoleTypeEnum.DIRECTOR], [UserRoleTypeEnum.SUPER_ADMIN]),
    ],
)
async def test_can_delete_user_successful(
    user_to_delete_roles: list[UserRoleTypeEnum], current_user_roles: list[UserRoleTypeEnum], session: AsyncSession
):
    current_user, user_to_delete = await create_test_users(
        current_user_roles=current_user_roles, target_user_roles=user_to_delete_roles
    )

    result = await can_delete_user(
        user_id=user_to_delete.id, current_user=current_user, user_service=UserService(session=session)
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_to_delete_roles, current_user_roles",
    [
        ([UserRoleTypeEnum.SUPER_ADMIN], [UserRoleTypeEnum.ADMIN]),
        ([UserRoleTypeEnum.ADMIN], [UserRoleTypeEnum.ACTOR, UserRoleTypeEnum.ADMIN]),
        ([UserRoleTypeEnum.ACTOR], [UserRoleTypeEnum.DIRECTOR]),
        ([UserRoleTypeEnum.DIRECTOR], [UserRoleTypeEnum.ACTOR]),
        ([UserRoleTypeEnum.VIEWER], [UserRoleTypeEnum.ACTOR]),
    ],
)
async def test_can_delete_user_access_error(
    user_to_delete_roles: list[UserRoleTypeEnum], current_user_roles: list[UserRoleTypeEnum], session: AsyncSession
):
    current_user, user_to_delete = await create_test_users(
        current_user_roles=current_user_roles, target_user_roles=user_to_delete_roles
    )

    with pytest.raises(AccessError):
        await can_delete_user(
            user_id=user_to_delete.id, current_user=current_user, user_service=UserService(session=session)
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_roles", [[UserRoleTypeEnum.DIRECTOR], [UserRoleTypeEnum.ACTOR], [UserRoleTypeEnum.VIEWER]]
)
async def test_can_delete_user_itself_successful(user_roles: list[UserRoleTypeEnum], session: AsyncSession):
    current_user = await UserFactory.create_async(user_roles=user_roles)

    result = await can_delete_user(
        user_id=current_user.id, current_user=current_user, user_service=UserService(session=session)
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize("user_roles", [[UserRoleTypeEnum.SUPER_ADMIN], [UserRoleTypeEnum.ADMIN]])
async def test_can_delete_user_itself_access_error(user_roles: list[UserRoleTypeEnum], session: AsyncSession):
    current_user = await UserFactory.create_async(user_roles=user_roles)

    with pytest.raises(AccessError):
        await can_delete_user(
            user_id=current_user.id, current_user=current_user, user_service=UserService(session=session)
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_to_update_roles, current_user_roles",
    [
        ([UserRoleTypeEnum.ADMIN], [UserRoleTypeEnum.SUPER_ADMIN]),
        ([UserRoleTypeEnum.ACTOR], [UserRoleTypeEnum.SUPER_ADMIN]),
        ([UserRoleTypeEnum.DIRECTOR], [UserRoleTypeEnum.SUPER_ADMIN]),
    ],
)
async def test_can_update_user_successful(
    user_to_update_roles: list[UserRoleTypeEnum], current_user_roles: list[UserRoleTypeEnum], session: AsyncSession
):
    current_user, user_to_update = await create_test_users(
        current_user_roles=current_user_roles, target_user_roles=user_to_update_roles
    )

    result = await can_edit_user(
        user_id=user_to_update.id,
        user=UserUpdate(user_roles=[UserRoleTypeEnum.VIEWER]),
        current_user=current_user,
        user_service=UserService(session=session),
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "current_user_roles", [[UserRoleTypeEnum.ACTOR], [UserRoleTypeEnum.VIEWER], [UserRoleTypeEnum.SUPER_ADMIN]]
)
async def test_can_update_user_itself_successful(current_user_roles: list[UserRoleTypeEnum], session: AsyncSession):
    current_user = await UserFactory.create_async(user_roles=current_user_roles)

    result = await can_edit_user(
        user_id=current_user.id,
        user=UserUpdate(first_name=faker.first_name()),
        current_user=current_user,
        user_service=UserService(session=session),
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "current_user_roles", [[UserRoleTypeEnum.ACTOR], [UserRoleTypeEnum.VIEWER], [UserRoleTypeEnum.ADMIN]]
)
async def test_can_update_user_roles_failed(current_user_roles: list[UserRoleTypeEnum], session: AsyncSession):
    current_user = await UserFactory.create_async(user_roles=current_user_roles)

    with pytest.raises(AccessError):
        await can_edit_user(
            user_id=current_user.id,
            user=UserUpdate(user_roles=[UserRoleTypeEnum.VIEWER]),
            current_user=current_user,
            user_service=UserService(session=session),
        )


@pytest.mark.asyncio
async def test_can_update_user_roles(session: AsyncSession):
    current_user, user_to_update = await create_test_users(
        current_user_roles=[UserRoleTypeEnum.SUPER_ADMIN], target_user_roles=[UserRoleTypeEnum.ACTOR]
    )

    result = await can_edit_user(
        user_id=user_to_update.id,
        user=UserUpdate(user_roles=[UserRoleTypeEnum.ADMIN]),
        current_user=current_user,
        user_service=UserService(session=session),
    )
    assert result is None
