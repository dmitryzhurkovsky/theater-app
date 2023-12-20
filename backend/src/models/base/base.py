import re
from uuid import UUID, uuid4

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


@as_declarative()
class BaseModel:
    @classmethod
    @declared_attr
    def __tablename__(cls):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower() + "s"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()), nullable=False
    )
