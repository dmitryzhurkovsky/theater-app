from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserPerformanceRoleBase(BaseModel):
    user_id: UUID
    performance_role_id: UUID


class UserPerformanceRoleRead(UserPerformanceRoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class UserPerformanceRoleUpdate(BaseModel):
    user_id: UUID | None = None
    performance_role_id: UUID | None = None
