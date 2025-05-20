import os 

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings

DATABASE_URL = os.getenv(settings.database_url, "postgresql+asyncpg://admin:a1b2c3d4e5@postgresql:5432/directorydb")

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def get_session():
    async with async_session_maker() as session:
        yield session
