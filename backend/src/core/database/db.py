from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.src.core.config.settings import get_settings

settings = get_settings()

postgres_async_engine = create_async_engine(
    url=settings.POSTGRES_ASYNC_URL,
    pool_size=58,
    max_overflow=0,
    echo=False,
)

postgres_async_session = async_sessionmaker(
    postgres_async_engine, expire_on_commit=False
)
