from fastapi import FastAPI

from src.core.config.settings import settings
from src.core.exceptions import exception_handlers
from src.core.logger import Logger
from src.core.middlewares import add_middlewares
from src.endpoints import add_routes


def make_application() -> FastAPI:
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        redoc_url=settings.REDOC_URL,
        debug=settings.DEBUG,
        exception_handlers=exception_handlers,
    )

    add_middlewares(_app)
    add_routes(_app)

    return _app


app: FastAPI = make_application()


@app.on_event("startup")
async def startup_event():
    import logging

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.disabled = True

    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.disabled = True

    Logger(json_logs=settings.LOG_JSON_FORMAT, log_level=settings.LOG_LEVEL).setup_logging()
