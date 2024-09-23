from typing import AsyncGenerator
from json import dumps

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from src.core.settings import settings

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL_asyncpg,
    pool_recycle=1800,
    json_serializer=lambda obj: dumps(obj, ensure_ascii=False),
    echo=True,
)


async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except IntegrityError as ex:
            await session.rollback()
            raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
        except Exception as ex:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(ex))
        finally:
            await session.commit()