from typing import Protocol, Any

from sqlalchemy import cast, delete, update, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dal.schemas.channel import ChannelORM


class IChannelDAL(Protocol):

    @staticmethod
    async def get_all(db_session: AsyncSession) -> list[ChannelORM] | None: ...

    @staticmethod
    async def get_by_id(
            db_session: AsyncSession, service_id: str
    ) -> ChannelORM | None: ...

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> ChannelORM | None: ...

    @staticmethod
    async def update(
            db_session: AsyncSession, service_id: str, **kwargs: Any
    ) -> ChannelORM | None: ...

    @staticmethod
    async def delete(
            db_session: AsyncSession, service_id: str
    ) -> ChannelORM | None: ...


class ChannelDAL(IChannelDAL):

    @staticmethod
    async def get_all(db_session: AsyncSession) -> list[ChannelORM] | None:
        stmt = select(ChannelORM).order_by(ChannelORM.channel_id)
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchall()
        if res:
            return [row[0] for row in res]
        return None

    @staticmethod
    async def get_by_id(db_session: AsyncSession, channel_id: str) -> ChannelORM | None:
        stmt = select(ChannelORM).where(ChannelORM.service_id == channel_id)
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchone()
        if res:
            return cast(ChannelORM, res[0])
        return None

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> ChannelORM | None:
        stmt = (
            insert(ChannelORM)
            .values(**kwargs)
            .on_conflict_do_update(index_elements=[ChannelORM.channel_id], set_=kwargs)
            .returning(ChannelORM)
        )
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchone()
        if res:
            return cast(ChannelORM, res[0])
        return None

    @staticmethod
    async def update(
            db_session: AsyncSession, channel_id: str, **kwargs: Any
    ) -> ChannelORM | None:
        stmt = (
            update(ChannelORM)
            .where(ChannelORM.channel_id == channel_id)
            .values(kwargs)
            .returning(ChannelORM)
        )
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchone()
        if res:
            return cast(ChannelORM, res[0])
        return None

    @staticmethod
    async def delete(db_session: AsyncSession, channel_id: str) -> ChannelORM | None:
        stmt = (
            delete(ChannelORM)
            .where(ChannelORM.channel_id == channel_id)
            .returning(ChannelORM)
        )
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchone()
        if res:
            return cast(ChannelORM, res[0])
        return None
