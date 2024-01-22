from fastapi import FastAPI

from src.core.config.settings import settings


def add_cors_middleware(app: FastAPI) -> dict[str, list[str] | bool]:
    allow_origins = [str(origin) for origin in settings.CORS_SETTINGS.ALLOW_ORIGINS]
    allow_headers = [str(header) for header in settings.CORS_SETTINGS.ALLOW_HEADERS]
    allow_methods = [str(header) for header in settings.CORS_SETTINGS.ALLOW_METHODS]
    allow_credentials = settings.CORS_SETTINGS.ALLOW_CREDENTIALS

    if app.debug:
        allow_origins = ["*"]
        allow_headers = ["*"]
        allow_methods = ["*"]
        allow_credentials = True

    return {
        "allow_origins": allow_origins,
        "allow_headers": allow_headers,
        "allow_methods": allow_methods,
        "allow_credentials": allow_credentials,
    }
