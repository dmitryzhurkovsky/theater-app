from typing import Any, Sequence, TypeVar

import structlog
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.utils import get_by
from src.core.enums import SortOrder
from src.core.exceptions import NotFoundError
from src.models import BaseModel
from src.utils import OnlyFieldsQueryBuilder

T = TypeVar("T", bound=BaseModel)

LOG = structlog.get_logger()


class BaseDatabaseManager:
    model: type[T]
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _handle_integrity_error(self, e: IntegrityError, session: AsyncSession) -> None:
        # Handle foreign key constraint errors, etc...
        await session.rollback()
        if e and "UniqueViolationError" in e.orig.args[0]:
            LOG.warning(f"IntegrityError for model -> {self.model.__name__}", exc_info=e)
        else:
            raise

    @property
    def base_query(self):
        return select(self.model)

    def get_query_fields(self, query, fields: list[str]):
        return OnlyFieldsQueryBuilder(self.model, fields).build(query)

    def get_by(self, query, filters: dict[str, Any]):
        """Provides query modification based on passed filters argument"""
        return get_by(self.model, query=query, criteria=filters)

    async def get(self, id_: int) -> T:
        """Retrieve an object by its ID"""
        stmt = select(self.model).where(self.model.id == id_)
        result = await self.session.execute(stmt)

        return result.scalar()

    async def get_or_404(self, uuid_: UUID, session: AsyncSession = None) -> T:
        """Retrieve an object by its ID and Raise NotFoundError if not found."""
        session = session or self.session

        try:
            result = await session.execute(select(self.model).filter_by(id=uuid_))
            instance = result.scalar_one()
        except NoResultFound:
            raise NotFoundError(detail=f"{self.model.__name__} with id:{uuid_} not found.") from None

        return instance

    async def create(self, obj_data: dict[str, Any], session: AsyncSession = None) -> T:
        """Create a new object."""
        session = session or self.session
        obj = self.model(**obj_data)

        session.add(obj)

        await session.commit()
        await session.refresh(obj)

        return obj

    async def update(self, uuid_: UUID, update_data: dict[str, Any], session: AsyncSession = None) -> T:
        """Update an object by its ID."""
        session = session or self.session
        instance = await self.get_or_404(uuid_, session)

        for key, value in update_data.items():
            setattr(instance, key, value)

        try:
            await session.commit()
            await session.refresh(instance)
        except IntegrityError as e:
            await self._handle_integrity_error(e, session)

        return instance

    async def upsert(self, id_: int, obj_data: dict[str, Any], session: AsyncSession = None) -> T:
        """Update an object if it exists, otherwise create it."""
        session = session or self.session

        try:
            await self.get_or_404(id_, session)
        except NotFoundError:
            obj_data["id"] = id_

            return await self.create(obj_data, session=session)
        else:
            return await self.update(id_, obj_data, session=session)

    async def delete(self, obj_uuid: UUID, session: AsyncSession = None) -> T:
        """Delete an object by its ID."""
        session = session or self.session
        instance = await self.get_or_404(obj_uuid, session)

        await session.delete(instance)
        await session.commit()

        return instance

    async def _list(
        self,
        fields: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_by: str | None = None,
        order: SortOrder | None = None,
        session: AsyncSession = None,
    ) -> Sequence[T]:
        """List objects with optional filters, limit, offset, and sort parameters.
        ⚠️ Basically this method MUST NOT be used in normal development (aka used in services or other DB managers).
        ⚠️ This method is done mostly for usage in tests and special cases
        ⚠️ This is not the main method to implement PAGINATION
        """
        session = session or self.session
        query = self.base_query

        if fields:
            query = self.get_query_fields(query, fields)

        if filters:
            query = self.get_by(query, filters)

        if sort_by:
            sort_column = getattr(self.model, sort_by, None)
            if sort_column:
                query = query.order_by(sort_column.asc() if order == SortOrder.ASC else sort_column.desc())

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        result = await session.execute(query)
        return result.scalars().all() if not fields else result.mappings().all()
