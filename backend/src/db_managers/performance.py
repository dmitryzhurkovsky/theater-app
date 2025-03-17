from datetime import date
from typing import Sequence
from uuid import UUID

from sqlalchemy import Subquery, all_, and_, func, select, union_all
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import literal_column

from src.db_managers.base import BaseDatabaseManager
from src.models import (
    Performance,
    PerformanceRole,
    User,
    UserPerformanceRoleRelationship,
)


class PerformanceManager(BaseDatabaseManager):
    model = Performance

    async def get_available_performances(self, day: date) -> Sequence[Performance]:
        """
        Args:
            day: date - day at which we want to hold a performance.
        Returns:
            All performances that have at least one cast available on this day.
        """
        available_roles_subquery = self.available_roles_subquery(day=day)

        stmt = (
            self.base_query.join(PerformanceRole)
            .group_by(self.model.id)
            .having(
                func.count(PerformanceRole.id)
                == select(func.count()).select_from(available_roles_subquery).scalar_subquery()
            )
            .options(joinedload(Performance.performance_roles))
        )

        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    @staticmethod
    def available_roles_subquery(day: date) -> Subquery:
        """
        Args:
            day: date - day at which we want to hold a performance.
        Returns:
            Subquery, that contains all roles of the particular performance that have at least one actor available at this day.
        """
        return (
            select(1)
            .select_from(PerformanceRole)
            .join(UserPerformanceRoleRelationship)
            .join(User)
            .where(
                and_(
                    PerformanceRole.performance_id == literal_column("performances.id"),
                    day != all_(func.coalesce(User.unavailable_dates, [])),
                )
            )
            .group_by(PerformanceRole.id)
            .subquery()
        )

    async def get_performance_participants_ids(self, performance_id: UUID) -> Sequence[UUID]:
        """Method that returns director_id along with actors ids who playing in the performance."""
        stmt1 = select(self.model.director_id.label("user_id")).where(self.model.id == performance_id)
        stmt2 = (
            select(UserPerformanceRoleRelationship.user_id)
            .join(PerformanceRole)
            .where(PerformanceRole.performance_id == performance_id)
        )

        result = await self.session.execute(union_all(stmt1, stmt2))
        return result.scalars().all()
