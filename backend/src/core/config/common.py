from urllib.parse import quote_plus

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from src.core.enums import LogLevelEum

POSTGRESQL_PATTERN = "postgresql+{}://{}:{}@{}:{}/{}"
CORS_ALLOW_ALL = '["*"]'


class Settings(BaseSettings):
    # Core settings
    VERSION: str = "1.0.0"
    PROJECT_NAME: str = "Theater API"
    ENDPOINTS_SERVICE_PREFIX: str = "/api"
    DEBUG: bool = True

    # Swagger settings
    DOCS_URL: str = f"{ENDPOINTS_SERVICE_PREFIX}/docs"
    OPENAPI_URL: str = f"{ENDPOINTS_SERVICE_PREFIX}/openapi.json"
    REDOC_URL: str = f"{ENDPOINTS_SERVICE_PREFIX}/redoc"

    # Database settings
    DB_HOST: str = "theater_db"
    DB_PORT: str = "5432"
    DB_USER: str = "docker"
    DB_PASS: str = "docker"
    DB_NAME: str = "theater_db"
    DB_INTERFACE_ENGINE: str = "asyncpg"
    DB_ECHO: bool = True
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_PRIMARY: PostgresDsn = f"postgresql+{DB_INTERFACE_ENGINE}://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Common settings
    SUPPORTED_LANGUAGES: list[str]
    SECRET_KEY: str | None = None

    # CORS settings
    ALLOW_ORIGINS: list[str] = CORS_ALLOW_ALL
    ALLOW_HEADERS: list[str] = CORS_ALLOW_ALL
    ALLOW_METHODS: list[str] = CORS_ALLOW_ALL
    ALLOW_CREDENTIALS: bool = True

    # Logs settings
    LOG_LEVEL: LogLevelEum = "INFO"
    LOG_JSON_FORMAT: bool = False
    LOG_REQUEST_QUERY_PARAMS: bool = False
    LOG_REQUEST_PATH_PARAMS: bool = False
    LOG_REQUEST_HEADERS: bool = False
    LOG_REQUEST_BODY: bool = False
    LOG_REQUEST_BODY_NORMALISED: bool = False
    LOG_REQUEST_USER: bool = False

    class Config:
        case_sensitive = True
        extra = "ignore"
