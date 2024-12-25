from uuid import UUID, uuid4

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, mapped_column


@as_declarative()
class BaseModel:
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
