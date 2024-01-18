from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import (
    PaginationMetaSchema,
    PaginationResponseSchema,
    QueryParameters,
    SortField,
)
from src.utils.query_builder import (
    OrderQueryBuilder,
    PaginationQueryBuilder,
    PaginatorConfig,
)


class Sorter:
    def __init__(self, model) -> None:
        self.model = model

    def apply(self, stmt: Select, sort: list[SortField]) -> Select:
        return OrderQueryBuilder(self.model, sort).build(stmt)


class Paginator:
    def __init__(self, default_per_page: int, max_per_page: int) -> None:
        self.default_per_page = default_per_page
        self.max_per_page = max_per_page

    def apply(self, stmt: Select, page: int | None, per_page: int | None) -> Select:
        config = self.get_config(page, per_page)
        pagination_builder = PaginationQueryBuilder(config)
        stmt = pagination_builder.build(stmt)

        return stmt

    def get_config(self, page: int | None, per_page: int | None) -> PaginatorConfig:
        config = PaginatorConfig(
            page,
            per_page,
            default_per_page=self.default_per_page,
            max_per_page=self.max_per_page,
        )

        return config


class RequestQueryHandler:
    def __init__(self, session: AsyncSession, model, default_per_page=100, max_per_page=200) -> None:
        self.session = session
        self.model = model
        self.sorter = Sorter(self.model)
        self.paginator = Paginator(default_per_page=default_per_page, max_per_page=max_per_page)

    def apply_sort(self, stmt: Select, query_params: QueryParameters) -> Select:
        if query_params.sort:
            stmt = self.sorter.apply(stmt, query_params.sort)

        return stmt

    def apply_pagination(self, stmt: Select, query_params: QueryParameters) -> Select:
        stmt = self.paginator.apply(stmt, query_params.page, query_params.per_page)

        return stmt

    async def get_paginated_response(self, stmt: Select, query_params: QueryParameters) -> PaginationResponseSchema:
        stmt = self.apply_sort(stmt, query_params)

        metadata = await self.get_pagination_metadata(
            stmt, self.paginator.get_config(query_params.page, query_params.per_page)
        )

        stmt = self.apply_pagination(stmt, query_params)

        result = await self.session.execute(stmt)

        return PaginationResponseSchema(
            data=result.scalars().all(),
            meta=metadata,
        )

    async def get_pagination_metadata(self, stmt: Select, paginator: PaginatorConfig) -> PaginationMetaSchema:
        """
        Get pagination related metadata.
        """
        stmt = stmt.with_only_columns(func.count()).order_by(None)
        result = await self.session.execute(stmt)

        total_items = result.scalar_one()
        total_pages = total_items // paginator.per_page + (total_items % paginator.per_page > 0)

        next_page = paginator.page + 1 if paginator.page < total_pages else None
        prev_page = paginator.page - 1 if paginator.page > 1 else None

        return PaginationMetaSchema(
            **{
                "per_page": paginator.per_page,
                "page": paginator.page,
                "total": total_items,
                "pages": total_pages,
                "page_number": paginator.page,
                "next_page": next_page,
                "prev_page": prev_page,
            }
        )
