import random
from datetime import date, timedelta

import pytest

from src.core.exceptions import QueryParamsBuilderException
from src.core.schemas import AvailablePerformanceQueryParameters


def test_previous_day_for_available_performance():
    with pytest.raises(QueryParamsBuilderException, match="day field cannot contain previous date"):
        AvailablePerformanceQueryParameters(day=date.today() - timedelta(days=random.randint(1, 5)))
