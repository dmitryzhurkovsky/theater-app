import structlog
from fastapi import status
from src.core.config.settings import settings
from src.core.exceptions import ApplicationException
from starlette.requests import Request
from starlette.responses import JSONResponse

LOG = structlog.stdlib.get_logger()


async def _handle_server_error(request: Request, err: Exception) -> JSONResponse:
    """Handle server errors and return formatted response."""

    _ = request
    LOG.error(
        "Server error occurred, with the following info: ",
        exc_info=err,
    )

    error_response_model = ApplicationException(
        detail="Internal Server Error! Sorry, something went wrong on our server."
    )

    return JSONResponse(
        error_response_model.model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def server_exception_middleware(request: Request, call_next) -> JSONResponse:
    """Middleware to handle server exceptions."""

    if settings.DEBUG:
        return await call_next(request)

    try:
        response = await call_next(request)
        return response
    except Exception as err:
        return await _handle_server_error(request, err)
