import structlog
from fastapi import status
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from src.core.config.settings import settings
from src.core.exceptions import ApplicationException

LOG = structlog.stdlib.get_logger()


async def _handle_server_error(request: Request, err: Exception) -> ORJSONResponse:
    """Handle server errors and return formatted response."""

    _ = request
    LOG.error(
        "Server error occurred, with the following info: ",
        exc_info=err,
    )

    error_response_model = ApplicationException(
        detail="Internal Server Error! Sorry, something went wrong on our server."
    )

    return ORJSONResponse(
        error_response_model.model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def server_exception_middleware(request: Request, call_next) -> ORJSONResponse:
    """Middleware to handle server exceptions."""

    if settings.DEBUG:
        return await call_next(request)

    try:
        response = await call_next(request)
        return response
    except Exception as err:
        return await _handle_server_error(request, err)
