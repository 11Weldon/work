from sqlalchemy.ext.asyncio import AsyncSession

from src.dal.repos.channel import IChannelDAL, ChannelDAL
from src.dal.schemas.channel import ChannelORM


class ChannelService:
    def __init__(self, dal: IChannelDAL):
        self.dal: IChannelDAL = dal

    async def add_channel(self, session: AsyncSession, channel_data):
        new_channel = ChannelORM(**channel_data.dict(exclude_unset=True))
        session.add(new_channel)
        await session.commit()
        await session.refresh(new_channel)
        return {"response": new_channel.channel_id}


channel_service = ChannelService(ChannelDAL)


def get_channel_service() -> ChannelService:
    return channel_service