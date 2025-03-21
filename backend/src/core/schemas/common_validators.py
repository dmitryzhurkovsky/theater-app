from datetime import date, datetime

from src.core.exceptions import QueryParamsBuilderException


def validate_day_is_not_previous(day: date | datetime, error_msg: str, is_query_param: bool = False) -> date | datetime:
    """Validate that provided day is not a previous."""
    exc_cls = QueryParamsBuilderException if is_query_param else ValueError
    value = day.date() if isinstance(day, datetime) else day

    if value < date.today():
        raise exc_cls(error_msg)

    return day
