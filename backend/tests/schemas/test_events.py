import random
from datetime import date, datetime, timedelta

import pytest

from src.core.exceptions import QueryParamsBuilderException
from tests.factories.schemas import (
    EventCreateSchemaFactory,
    EventQueryParametersSchemaFactory,
)


def test_previous_date_for_event():
    with pytest.raises(ValueError, match="date field cannot contain previous date"):
        EventCreateSchemaFactory.build(date=datetime.now() - timedelta(days=random.randint(1, 5)))


def test_provide_only_start_date():
    with pytest.raises(
        QueryParamsBuilderException, match="start_date and end_date fields should be provided together."
    ):
        EventQueryParametersSchemaFactory.build(start_date=date.today(), end_date=None)


def test_provide_only_end_date():
    with pytest.raises(
        QueryParamsBuilderException, match="start_date and end_date fields should be provided together."
    ):
        EventQueryParametersSchemaFactory.build(start_date=None, end_date=date.today())


def test_end_date_before_start_date():
    with pytest.raises(QueryParamsBuilderException, match="start_date should be before end_date."):
        EventQueryParametersSchemaFactory.build(
            start_date=date.today(), end_date=date.today() - timedelta(days=random.randint(1, 5))
        )
