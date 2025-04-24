import re
from datetime import date

from src.core.schemas.common_validators import validate_day_is_not_previous


def validate_unavailable_dates(value: list[date] | None) -> list[date] | None:
    if value:
        for free_date in value:
            validate_day_is_not_previous(
                day=free_date, error_msg=""" Field "unavailable_dates" cannot contain previous days """
            )

    return value


def check_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[0-9]", value):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[\W_]", value):
        raise ValueError("Password must contain at least one special character")

    return value
