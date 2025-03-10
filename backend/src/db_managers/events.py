from datetime import date, datetime, time
from typing import Any
from uuid import UUID

from sqlalchemy.sql import Select

from src.db_managers.base import BaseDatabaseManager
from src.models import Event, EventConfirmation


class EventManager(BaseDatabaseManager):
    model = Event

    def get_by(self, query: Select, filters: dict[str, Any]) -> Select:
        if "user_id" in filters:
            query = self.filter_by_user(query, user_id=filters.pop("user_id"))

        if "start_date" in filters and "end_date" in filters:
            query = self.filter_by_time_range(
                query, start_date=filters.pop("start_date"), end_date=filters.pop("end_date")
            )

        return super().get_by(query, filters)

    def filter_by_time_range(self, query: Select, start_date: date, end_date: date) -> Select:
        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)
        return query.where(self.model.date >= start_datetime, self.model.date <= end_datetime)

    @staticmethod
    def filter_by_user(query: Select, user_id: UUID) -> Select:
        """Filter events that a specific user is participating in."""
        return query.join(EventConfirmation).where(EventConfirmation.user_id == user_id)
