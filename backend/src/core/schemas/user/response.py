from src.core.schemas.base import BaseResponseSchema
from src.core.schemas.common import PaginationResponseSchema
from src.core.schemas.user.base import UserRead


class UserResponseSchema(BaseResponseSchema):
    data: UserRead


class UserListResponseSchema(PaginationResponseSchema):
    data: list[UserRead]
