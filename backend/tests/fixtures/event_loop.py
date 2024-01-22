import asyncio

import pytest

# We have asynchronous code in our tests (using async def functions and pytest.mark.asyncio),
# so we need an event loop to run and manage these asynchronous tasks.
# In other ways tests will not run.


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
