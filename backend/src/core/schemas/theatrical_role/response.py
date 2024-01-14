from src.core.schemas.base import BaseResponseSchema
from src.core.schemas.common import PaginationResponseSchema
from src.core.schemas.theatrical_role.base import TheatricalRoleRead


class TheatricalRoleResponseSchema(BaseResponseSchema):
    data: TheatricalRoleRead


class TheatricalRoleListResponseSchema(PaginationResponseSchema):
    data: list[TheatricalRoleRead]
