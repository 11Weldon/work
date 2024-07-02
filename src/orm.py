from typing import Dict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base, async_engine
from src.models.models import Domain


class AsyncORM:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


# async def add_channel(session: AsyncSession, title: str, id: int):
#     new_func = Channel(channel_id=id, channel_title=title)
#     session.add(new_func)
#     return new_func


async def create_domain(session: AsyncSession, title: Dict[str, str], descr: Dict[str, str]):
    try:
        new_domain = Domain(domain_title=title, domain_descr=descr)
        session.add(new_domain)
        await session.commit()
        return new_domain
    except IntegrityError as ex:
        await session.rollback()
        print(f"IntegrityError: {ex}")
        raise ex
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        await session.rollback()
        raise ex
