import os
from urllib.parse import quote_plus

from environs import Env
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from src.core.enums import EnvironmentEnum, LogLevelEum

POSTGRESQL_PATTERN = "postgresql+{}://{}:{}@{}:{}/{}"
CORS_ALLOW_ALL = '["*"]'

env = Env()
env.read_env(os.environ.get("ENV_FILE", None))


class DatabaseSettings(BaseSettings):
    DB_HOST: str = env.str("DB_HOST", "theater_db")
    DB_PORT: str = env.str("DB_PORT", "5432")
    DB_USER: str = env.str("DB_USER", "docker")
    DB_PASS: str = env.str("DB_PASS", "docker")
    DB_NAME: str = env.str("DB_NAME", "theater_db")
    DB_INTERFACE_ENGINE: str = "asyncpg"
    DB_ECHO: bool = env.bool("DB_ECHO", "True")
    DB_POOL_SIZE: int = env.int("DB_POOL_SIZE", "5")
    DB_MAX_OVERFLOW: int = env.int("DB_MAX_OVERFLOW", "10")
    DB_PRIMARY: PostgresDsn | str = (
        f"postgresql+{DB_INTERFACE_ENGINE}://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    class Config:
        case_sensitive = True


class CommonSetting(BaseSettings):
    SUPPORTED_LANGUAGES: list[str] = env.json("SUPPORTED_LANGUAGES", '["eng","ru"]')
    SECRET_KEY: str = env.str("SECRET_KEY", "you_secret_key")

    class Config:
        case_sensitive = True


class CORSSettings(BaseSettings):
    ALLOW_ORIGINS: list[str] = env.json("ALLOW_ORIGINS", CORS_ALLOW_ALL)
    ALLOW_HEADERS: list[str] = env.json("ALLOW_HEADERS", CORS_ALLOW_ALL)
    ALLOW_METHODS: list[str] = env.json("ALLOW_METHODS", CORS_ALLOW_ALL)
    ALLOW_CREDENTIALS: bool = env.bool("ALLOW_CREDENTIALS", "True")

    class Config:
        case_sensitive = True


class LogSettings(BaseSettings):
    LOG_LEVEL: LogLevelEum = env.str("LOG_LEVEL", "INFO")
    LOG_JSON_FORMAT: bool = env.bool("LOG_JSON_FORMAT", "False")
    LOG_REQUEST_QUERY_PARAMS: bool = env.bool("LOG_REQUEST_QUERY_PARAMS", "False")
    LOG_REQUEST_PATH_PARAMS: bool = env.bool("LOG_REQUEST_PATH_PARAMS", "False")
    LOG_REQUEST_HEADERS: bool = env.bool("LOG_REQUEST_HEADERS", "False")
    LOG_REQUEST_BODY: bool = env.bool("LOG_REQUEST_BODY", "False")
    LOG_REQUEST_BODY_NORMALISED: bool = env.bool("LOG_REQUEST_BODY_NORMALISED", "False")
    LOG_REQUEST_USER: bool = env.bool("LOG_REQUEST_USER", "False")

    class Config:
        case_sensitive = True


class Settings(BaseSettings):
    # Core settings
    VERSION: str = "1.0.0"
    PROJECT_NAME: str = "Theater API"
    ENDPOINTS_SERVICE_PREFIX: str = env.str("ENDPOINTS_SERVICE_PREFIX", "/api")
    DEBUG: bool = env.bool("DEBUG", "False")
    ENVIRONMENT: EnvironmentEnum = env.str("ENVIRONMENT", EnvironmentEnum.DEV.value)

    # Swagger settings
    DOCS_URL: str = f"{ENDPOINTS_SERVICE_PREFIX}/docs"
    OPENAPI_URL: str = f"{ENDPOINTS_SERVICE_PREFIX}/openapi.json"
    REDOC_URL: str = f"{ENDPOINTS_SERVICE_PREFIX}/redoc"

    # Database settings
    DATABASE_SETTINGS: DatabaseSettings = DatabaseSettings()

    # Common settings
    COMMON_SETTING: CommonSetting = CommonSetting()

    # CORS settings
    CORS_SETTINGS: CORSSettings = CORSSettings()

    # Logs settings
    LOG_SETTINGS: LogSettings = LogSettings()

    class Config:
        case_sensitive = True
