from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.enums import GenreTypeEnum


class PerformanceBase(BaseModel):
    title: str
    director_id: UUID
    image: str | None = None
    description: str | None = None
    about_author: str | None = None
    genre: GenreTypeEnum
    age: int = Field(default=0, ge=0)
    annotation: str | None = None
    recommendations: dict[str, Any] | None = None


class PerformanceRead(PerformanceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class PerformanceCreate(PerformanceBase):
    need_admin_approve: bool = False


class PerformanceUpdate(PerformanceBase):
    title: str | None = None
    director_id: UUID | None = None
    genre: GenreTypeEnum | None = None
    age: int | None = None
    neeneed_admin_approve: bool | None = None
