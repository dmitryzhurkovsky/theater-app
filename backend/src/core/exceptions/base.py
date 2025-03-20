from functools import wraps
from typing import Any

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, ConfigDict


def call_exception(cls):
    @wraps(cls)
    def inner(*args, **kwargs):
        return cls(status_code=cls.status_code, detail=cls.detail, *args, **kwargs)

    return inner


class ApplicationException(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    detail: str
    errors: list[Any] | None = None


class BaseError(HTTPException):
    status_code: int | None = 500
    detail: str = "Internal Server Error"

    def __init__(self, detail: str | None = None, status_code: int | None = None, *args, **kwargs):
        super().__init__(
            status_code=status_code if status_code else self.status_code,
            detail=detail if detail else self.detail,
            *args,
            **kwargs
        )


class NotFoundError(BaseError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not Found"


class AccessError(BaseError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You don't have permission to access this resource"


class OperationFailedError(BaseError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Operation failed"
