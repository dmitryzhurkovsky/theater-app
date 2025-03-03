from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import CategoryTypeEnum, GenreTypeEnum
from src.core.schemas.common import PaginationResponseSchema, QueryParameters
from src.core.schemas.performance_role import PerformanceRoleRead


class PerformanceBase(BaseModel):
    title: str
    director_id: UUID
    image: str | None = None
    description: str | None = Field(max_length=1024, default=None)
    about_author: str | None = Field(max_length=1024, default=None)
    genre: list[GenreTypeEnum]
    category: CategoryTypeEnum
    age: int = Field(default=0, ge=0)
    annotation: str | None = Field(max_length=1024, default=None)
    recommendations: dict[str, Any] | None = None


class PerformanceRead(PerformanceBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    director_id: UUID | None
    created_at: datetime
    updated_at: datetime
    performance_roles: list[PerformanceRoleRead] = []


class PerformanceCreate(PerformanceBase):
    need_admin_approve: bool = False


class PerformanceUpdate(PerformanceBase):
    title: str | None = None
    director_id: UUID | None = None
    genre: list[GenreTypeEnum] | None = None
    category: CategoryTypeEnum | None = None
    age: int | None = None
    need_admin_approve: bool | None = None


class PerformanceQueryParameters(QueryParameters):
    category: CategoryTypeEnum | None = None


class PerformancePaginationResponseSchema(PaginationResponseSchema):
    data: list[PerformanceRead]
