from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VERSION: str = "1.0.0"

    DEBUG: bool = True

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_ASYNC_URL: str

    SUPPORTED_LANG: list[str]
    SECRET_KEY: str | None = None

    model_config = SettingsConfigDict(extra="ignore")
