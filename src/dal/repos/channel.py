from typing import Protocol, Any, cast

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dal.schemas.channel import ChannelORM
from src.models.channel import ChannelModel
from sqlalchemy.dialects.postgresql import insert

class IChannelDAL(Protocol):

    @staticmethod
    async def get_all(db_session: AsyncSession) -> list[ChannelModel] | None: ...

    @staticmethod
    async def get_by_id(
            db_session: AsyncSession, service_id: str
    ) -> ChannelModel | None: ...

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> ChannelModel | None: ...

    @staticmethod
    async def update(
            db_session: AsyncSession, service_id: str, **kwargs: Any
    ) -> ChannelModel | None: ...

    @staticmethod
    async def delete(
            db_session: AsyncSession, service_id: str
    ) -> ChannelModel | None: ...


class ChannelDAL(IChannelDAL):

    @staticmethod
    async def get_all(db_session: AsyncSession) -> list[ChannelModel] | None:
        stmt = select(ChannelORM).order_by(ChannelORM.channel_id)
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchall()
        if res:
            return [row[0] for row in res]
        return None

    @staticmethod
    async def get_by_id(db_session: AsyncSession, channel_id: str) -> ChannelModel | None:
        stmt = select(ChannelORM).where(ChannelORM.channel_id == channel_id)
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchone()
        if res:
            return cast(ChannelModel, res[0])
        return None

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> ChannelModel | None:
        stmt = (
            insert(ChannelORM)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=[ChannelORM.channel_id],
                set_=kwargs)
            .returning(ChannelORM)
        )
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchone()
        if res:
            return cast(ChannelModel, res[0])
        return None

    @staticmethod
    async def update(
            db_session: AsyncSession, channel_id: str, **kwargs: Any
    ) -> ChannelModel | None:
        stmt = (
            update(ChannelORM)
            .where(ChannelORM.channel_id == channel_id)
            .values(kwargs)
            .returning(ChannelORM)
        )
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchone()
        if res:
            return cast(ChannelModel, res[0])
        return None

    @staticmethod
    async def delete(db_session: AsyncSession, channel_id: str) -> ChannelModel | None:
        stmt = (
            delete(ChannelORM)
            .where(ChannelORM.channel_id == channel_id)
            .returning(ChannelORM)
        )
        stmt_exec = await db_session.execute(stmt)
        res = stmt_exec.fetchone()
        if res:
            return cast(ChannelModel, res[0])
        return None
