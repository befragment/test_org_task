import os 

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings

Base = declarative_base()

engine = create_async_engine(settings.database_url, echo=True)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def get_session():
    async with async_session_maker() as session:
        yield session
