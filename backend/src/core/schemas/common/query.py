from pydantic import BaseModel, field_validator

from src.core.enums.sort_order import SortOrder
from src.core.schemas.common.pagination import Pagination


class SortField(BaseModel):
    """Query parameters for sorting."""

    field: str | None = None
    order: SortOrder | None = SortOrder.ASC  # asc or desc

    @staticmethod
    def from_string(s: str) -> "SortField":
        parts = s.split(":")
        if len(parts) == 2:
            return SortField(field=parts[0], order=parts[1])
        return SortField(field=parts[0])

    @field_validator("order", mode="before")
    def validate_order(cls, v):  # noqa
        return v.lower() if v in ["asc", "desc"] else "asc"


class QueryParameters(Pagination):
    """Query parameters for sorting and pagination."""

    sort: list[SortField] | None = []

    @field_validator("sort", mode="before")
    def parse_sort(cls, v: str | None = None) -> list[SortField]:  # noqa
        if not v or not isinstance(v, str):
            return []
        return [SortField.from_string(part) for part in v.split(",")]
