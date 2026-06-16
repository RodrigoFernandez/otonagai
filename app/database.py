from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

# Creación del motor asíncrono de SQLAlchemy
engine = create_async_engine(settings.database_url, echo=False)
# Fábrica de sesiones asíncronas
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependencia que provee una sesión de base de datos por request
async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
