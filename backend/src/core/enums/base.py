from enum import Enum, unique
from functools import lru_cache
from operator import attrgetter


@unique
class BaseEnum(str, Enum):
    @classmethod
    @lru_cache(None)
    def values(cls) -> tuple:
        return tuple(map(attrgetter("value"), cls))

    @classmethod
    @lru_cache(None)
    def names(cls) -> tuple:
        return tuple(map(attrgetter("name"), cls))

    @classmethod
    @lru_cache(None)
    def items(cls) -> tuple:
        return tuple(zip(cls.values(), cls.names()))

    @classmethod
    @lru_cache(None)
    def revert_items(cls) -> tuple:
        return tuple(zip(cls.names(), cls.values()))

    @classmethod
    @lru_cache(None)
    def members(cls) -> dict:
        return dict(cls.items())

    @classmethod
    @lru_cache(None)
    def revert_members(cls) -> dict:
        return dict(cls.revert_items())
