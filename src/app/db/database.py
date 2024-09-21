from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import config

sync_engine = create_engine(url=config.sync_database_url)  # type: ignore
engine = create_async_engine(
    url=config.database_url,  # type: ignore
    echo=config.service.db_echo,  # type: ignore
)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session():
    """Async sessions generator."""
    async with async_session() as session:
        yield session
