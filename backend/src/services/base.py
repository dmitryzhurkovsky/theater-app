from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import ControllerConfig, PaginationResponseSchema, QueryParameters, Pagination
from src.utils.query_builder.request_query_handler import RequestQueryHandler


class BaseService:
    def __init__(self, session: AsyncSession, config: ControllerConfig = None) -> None:
        self.session = session
        self.config = config

    async def get_paginated_response(self, model, stmt: Select) -> PaginationResponseSchema:
        pagination = Pagination(page=1, per_page=10)
        query_parameters = QueryParameters(pagination=pagination)
        query_enhancer = RequestQueryHandler(
            self.session,
            model,
            default_per_page=self.config.pagination.default_per_page,
            max_per_page=self.config.pagination.max_per_page,
        )
        return await query_enhancer.get_paginated_response(stmt, query_parameters)
