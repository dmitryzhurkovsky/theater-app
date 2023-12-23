import structlog
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from src.core.config.settings import settings
from src.core.exceptions.base import ApplicationException
from starlette.requests import Request
from starlette.responses import JSONResponse

LOG = structlog.stdlib.get_logger()


async def custom_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    _ = request
    if settings.DEBUG:
        LOG.error(
            "Validation error occurred, with the following info: ",
            exc_info=exc,
        )

    return JSONResponse(
        ApplicationException(
            detail="Request Body Validation error",
            errors=jsonable_encoder(exc.errors()),
        ).model_dump(),
        status_code=status.HTTP_400_BAD_REQUEST,
    )
