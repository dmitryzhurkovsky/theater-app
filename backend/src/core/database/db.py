from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config.settings import settings

postgres_async_engine = create_async_engine(
    url=settings.DATABASE_SETTINGS.DB_PRIMARY,
    pool_size=settings.DATABASE_SETTINGS.DB_POOL_SIZE,
    max_overflow=settings.DATABASE_SETTINGS.DB_MAX_OVERFLOW,
    echo=settings.DATABASE_SETTINGS.DB_ECHO,
)

postgres_async_session = async_sessionmaker(postgres_async_engine, expire_on_commit=False)
