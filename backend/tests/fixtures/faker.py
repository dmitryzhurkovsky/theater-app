import pytest


# this needs to the future faker usage
@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return 0
