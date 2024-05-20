from src.core.schemas.common import PaginationResponseSchema
from src.core.schemas.user.base import UserRead


class UserListResponseSchema(PaginationResponseSchema):
    data: list[UserRead]
