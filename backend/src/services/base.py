from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import ControllerConfig, PaginationResponseSchema, QueryParameters
from src.utils.query_builder.request_query_handler import RequestQueryHandler


class BaseService:
    def __init__(self, session: AsyncSession, config: ControllerConfig = None) -> None:
        self.session = session
        self.config = config

    async def get_paginated_response(
        self, model, stmt: Select, query_parameters: QueryParameters
    ) -> PaginationResponseSchema:
        query_enhancer = RequestQueryHandler(
            self.session,
            model,
            default_per_page=self.config.pagination.default_per_page,
            max_per_page=self.config.pagination.max_per_page,
        )
        return await query_enhancer.get_paginated_response(stmt, query_parameters)
