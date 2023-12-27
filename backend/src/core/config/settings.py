import platform
from functools import cache

from src.core.config.common import Settings
from src.core.config.utils.env_helper import get_env


@cache
def get_settings() -> Settings:
    env_file = get_env(platform.system().lower())
    return Settings(_env_file=env_file)


settings: Settings = get_settings()
