import random
from datetime import date, timedelta

import pytest

from tests.factories.schemas import UserCreateSchemaFactory, UserRegisterSchemaFactory


def test_password_short():
    with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
        UserRegisterSchemaFactory.build(password="Short1!")


def test_password_no_uppercase():
    with pytest.raises(ValueError, match="Password must contain at least one uppercase letter"):
        UserRegisterSchemaFactory.build(password="lowercase!...1")


def test_password_no_lowercase():
    with pytest.raises(ValueError, match="Password must contain at least one lowercase letter"):
        UserRegisterSchemaFactory.build(password="UPPERCASE!...1")


def test_password_no_digit():
    with pytest.raises(ValueError, match="Password must contain at least one digit"):
        UserRegisterSchemaFactory.build(password="NoDigit!")


def test_password_no_special_symbol():
    with pytest.raises(ValueError, match="Password must contain at least one special character"):
        UserRegisterSchemaFactory.build(password="NoSpecial1")


def test_previous_unavailable_dates():
    with pytest.raises(ValueError, match=""" Field "unavailable_dates" cannot contain previous days """):
        UserCreateSchemaFactory.build(
            unavailable_dates=[date.today() - timedelta(days=i) for i in range(1, random.randint(2, 5))]
        )
