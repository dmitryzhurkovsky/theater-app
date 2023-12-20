from enum import Enum, unique
from functools import lru_cache
from operator import attrgetter


@unique
class BaseEnum(Enum):
    @classmethod
    @lru_cache(None)
    def values(cls):
        return tuple(map(attrgetter("value"), cls))


class GenderTypeEnum(str, BaseEnum):
    MAN = 'man'
    WOMAN = 'woman'


class RoleTypeEnum(str, BaseEnum):
    ADMIN = 'admin'
    ACTOR = 'actor'
    VIEWER = 'viewer'
