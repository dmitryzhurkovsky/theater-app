import re
from uuid import UUID, uuid4

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


@as_declarative()
class BaseModel:
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: str(uuid4()), nullable=False)
