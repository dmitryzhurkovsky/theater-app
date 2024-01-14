from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

if TYPE_CHECKING:
    from src.models.users import User


class TheatricalRoleBase(BaseModel):
    name: str


class TheatricalRoleRead(TheatricalRoleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    actors: list["User"]  # TODO need to replace it with Pydantic model

    class Config:
        from_attributes = True


class TheatricalRoleCreate(TheatricalRoleBase):
    actors: list[int] | None = None


class TheatricalRoleUpdate(TheatricalRoleBase):
    name: str | None = None
    actors: list[int] | None = None
