from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import get_db
from app.main import app
from app.models.base import Base

# SQLite en memoria con cache compartido para que múltiples conexiones
# (engine → sesiones) vean los mismos datos durante el test
TEST_DB_URL = "sqlite+aiosqlite:///file:test_shared?mode=memory&cache=shared&uri=true"
test_engine = create_async_engine(TEST_DB_URL)
test_async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Crea todas las tablas antes de cada test y las elimina al final,
    asegurando aislamiento total entre tests."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Sobrescribe la dependencia get_db de FastAPI para que los endpoints
# usen la base de datos de tests en lugar de la base real
async def override_get_db() -> AsyncGenerator[AsyncSession]:
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    """Cliente HTTP asíncrono contra la app FastAPI en modo test,
    listo para enviar requests sin necesidad de un servidor real."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
