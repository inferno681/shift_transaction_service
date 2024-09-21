import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import create_database, drop_database

from config.config import config

config.service.db_name = 'test_db'  # type: ignore


@pytest.fixture(scope='session', autouse=True)
async def crate_and_drop_database():
    """Database preparation  before test.."""
    create_database(config.sync_database_url)

    engine = create_async_engine(url=config.database_url)
    async with engine.begin() as conn:
        await conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS "user"
            ("id" serial PRIMARY KEY,
            "login" varchar UNIQUE,
            "hashed_password" varchar,
            "balance" integer,
            "is_verified" bool DEFAULT false);
            """,
            ),
        )
        await conn.execute(
            text(
                """
            INSERT INTO "user" (login, hashed_password, balance)
            VALUES ('login', 'hashed_password', 1000);
            """,
            ),
        )
        await conn.commit()
        from app.db import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()
    drop_database(config.sync_database_url)
    await engine.dispose()


@pytest.fixture(scope='session')
def anyio_backend():
    """Backend for test."""
    return 'asyncio'


@pytest.fixture(scope='session')
async def client():
    """Client for testing."""
    from app.main import app

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://127.0.0.1:8000/api/',
        ) as client:
            yield client
