from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PerformanceRoleCreate(BaseModel):
    title: str
    performance_id: UUID


class PerformanceRoleRead(PerformanceRoleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class PerformanceRoleUpdate(BaseModel):
    title: str | None = None
    performance_id: UUID | None = None
