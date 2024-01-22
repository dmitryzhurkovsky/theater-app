from typing import Any

from sqlalchemy.sql import Select

from src.models import BaseModel


def get_by(table: BaseModel, query: Select, criteria: dict[str, Any]):
    """
    Get data by criteria

    :param table: Table model
    :param query: Query object
    :param criteria: Criteria to filter

    :return: Query
    """

    for name, value in criteria.items():
        if hasattr(table, name):
            query = (
                query.where(getattr(table, name) == value)
                if not isinstance(value, list)
                else query.where(getattr(table, name).in_(value))
            )
    return query
