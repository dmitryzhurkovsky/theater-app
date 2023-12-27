import structlog
from fastapi import Request, Response, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import HTTPException
from src.core.config.settings import settings
from starlette.responses import JSONResponse

LOG = structlog.stdlib.get_logger()


async def custom_http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse | Response:
    if settings.DEBUG:
        LOG.error(
            "Http error occurred, with the following info: ",
            exc_info=exc,
        )

    if exc.status_code == status.HTTP_200_OK:
        if isinstance(exc.detail, dict):
            body = exc.detail
        else:
            body = {"detail": exc.detail}
        return JSONResponse(body, status_code=exc.status_code)
    return await http_exception_handler(request, exc)
