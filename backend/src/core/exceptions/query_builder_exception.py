from fastapi import status

from src.core.exceptions.base import BaseError


class QueryBuilderException(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST


class PaginationBuilderException(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST
