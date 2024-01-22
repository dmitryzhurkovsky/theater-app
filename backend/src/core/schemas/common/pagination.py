from typing import Any

from pydantic import BaseModel, field_validator

from src.core.schemas.base import BaseResponseSchema


class PaginationMetaSchema(BaseResponseSchema):
    per_page: int
    total: int
    pages: int
    page_number: int
    next_page: str | None
    prev_page: str | None


class PaginationResponseSchema(BaseResponseSchema):
    data: list[Any]
    meta: PaginationMetaSchema


class Pagination(BaseModel):
    """Query parameters for pagination."""

    page: int | None = None
    per_page: int | None = None

    @field_validator("page_number", "per_page", mode="before", check_fields=False)
    def validate_page_number(cls, value):  # noqa
        if value is not None and value < 1:
            raise ValueError("""The fields "page_number" & "per_page" must be greater than 0.""")

        return value
