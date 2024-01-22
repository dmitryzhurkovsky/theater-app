from functools import cache

from src.core.config.common import Settings


@cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
