from src.core.enums.base import BaseEnum


class UserRoleTypeEnum(BaseEnum):
    VIEWER = "Viewer"
    ADMIN = "Admin"
    ACTOR = "Actor"
    DIRECTOR = "Director"
    SUPER_ADMIN = "Super Admin"
