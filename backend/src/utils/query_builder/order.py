from sqlalchemy import asc, desc
from sqlalchemy.sql import Select

from src.core.schemas.common.query import SortField
from src.utils.query_builder.fields import FieldParser

ORDER_BY_MAPPING = {
    "desc": desc,
    "asc": asc,
}


class OrderQueryBuilder:
    def __init__(self, model, sort: list[SortField]) -> None:
        self.model = model
        self.sort = sort

    def build(self, stmt: Select) -> Select:
        order = []

        for sort_field in self.sort:
            field_parser = FieldParser(self.model, sort_field.field)
            order.append(ORDER_BY_MAPPING[sort_field.order](field_parser.field))

        return stmt.order_by(*order) if order else stmt
