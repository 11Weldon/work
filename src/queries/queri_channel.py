from typing import Dict, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Channel, ChannelMapping


async def add_channel(session: AsyncSession, title: str, synopsis_short: Optional[Dict], synopsis_long: Optional[Dict],
                      keywords: Optional[Dict], audio: Optional[Dict]):
    new_channel = Channel(
        channel_title=title,
        synopsis_short=synopsis_short,
        synopsis_long=synopsis_long,
        keywords=keywords,
        audio=audio
    )

    session.add(new_channel)
    return new_channel


async def get_channel(session: AsyncSession) -> list[Channel]:
    result = await session.execute(select(Channel))
    return result.scalars().all()


async def add_channel_mapping(session: AsyncSession, channelId: int, targetId: int, type: str, mapped: str):
    try:
        new_mapping = ChannelMapping(channel_id=channelId, target_id=targetId, type=type, mapped=mapped)
        session.add(new_mapping)
        await session.commit()
        return {"result": 0}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


async def delete_channel(session: AsyncSession, channel_id: int):
    try:
        channel = await session.execute(select(Channel).filter_by(channel_id=channel_id))
        channel_obj = channel.scalar()
        if not channel_obj:
            print(f"Channel with ID {channel_id} not found.")
            return None

        await session.delete(channel_obj)
        await session.commit()
        print(f"Deleted Channel with ID {channel_id}.")
        return channel_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


async def update_channel_live_url(session: AsyncSession, service_id: int, transport_id: int,
                                  rec_adapter_id: int, live_url: str, time_stamp: str):
    try:

        channel = await session.execute(
            select(Channel).filter_by(service_id=service_id, transport_id=transport_id,
                                      rec_adapter_id=rec_adapter_id)
        )
        channel_obj = channel.scalar()
        if not channel_obj:
            raise HTTPException(status_code=404, detail="Channel not found")

        channel_obj.live_url = live_url
        channel_obj.time_stamp = time_stamp

        await session.commit()
    except Exception as ex:
        await session.rollback()
        raise ex
