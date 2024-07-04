from starlette import status

from src.core.exceptions.base import BaseError


class UserAlreadyExistsException(BaseError):
    status_code = status.HTTP_409_CONFLICT
    title = "Conflict"
    detail = "User already exists"


class InvalidJWTException(BaseError):
    status_code = status.HTTP_401_UNAUTHORIZED
    title = "Unauthorized"
    detail = "Could not validate credentials"
