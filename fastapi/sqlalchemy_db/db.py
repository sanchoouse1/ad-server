from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


engine = create_async_engine(settings.DATABASE_URL_asyncpg)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

async def get_async_session():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass