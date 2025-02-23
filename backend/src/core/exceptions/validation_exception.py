import structlog
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from src.core.config.settings import settings
from src.core.exceptions.base import ApplicationException

LOG = structlog.stdlib.get_logger()


async def custom_validation_exception_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
    _ = request
    if settings.DEBUG:
        LOG.error(
            "Validation error occurred, with the following info: ",
            exc_info=exc,
        )

    return ORJSONResponse(
        ApplicationException(
            detail="Request Body Validation error",
            errors=jsonable_encoder(exc.errors()),
        ).model_dump(),
        status_code=status.HTTP_400_BAD_REQUEST,
    )
