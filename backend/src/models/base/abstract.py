from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import Mapped, mapped_column


class TimestampAbstractModel(AbstractConcreteBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False,
    )
