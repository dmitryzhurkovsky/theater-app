import re
from uuid import UUID, uuid4

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


@as_declarative()
class BaseModel:
    __abstract__ = True

    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower() + "s"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: str(uuid4()), nullable=False)
