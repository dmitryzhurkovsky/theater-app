from fastapi.exceptions import HTTPException, RequestValidationError

from src.core.exceptions.base import AccessError, ApplicationException, NotFoundError
from src.core.exceptions.http_exception import custom_http_exception_handler
from src.core.exceptions.query_builder_exception import (
    PaginationBuilderException,
    QueryBuilderException,
)
from src.core.exceptions.validation_exception import custom_validation_exception_handler

exception_handlers = {
    RequestValidationError: custom_validation_exception_handler,
    HTTPException: custom_http_exception_handler,
}

__all__ = (
    "exception_handlers",
    "AccessError",
    "ApplicationException",
    "NotFoundError",
    "PaginationBuilderException",
    "QueryBuilderException",
)
