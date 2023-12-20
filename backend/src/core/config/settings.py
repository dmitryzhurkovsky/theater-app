import platform
from functools import lru_cache

from backend.src.core.config.common import Settings
from backend.src.core.config.utils.env_helper import get_env


@lru_cache
def get_settings() -> Settings:
    env_file = get_env(platform.system().lower())
    return Settings(_env_file=env_file)
