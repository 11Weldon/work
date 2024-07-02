from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..queries import queri_channel
from ..schema import ChannelSchema, ChannelMappingSchema

channel_router = APIRouter()


@channel_router.get("/channel/", response_model=list[ChannelSchema])
async def get_channel(session: AsyncSession = Depends(get_db)):
    try:
        channel = await queri_channel.get_channel(session)
        return [ChannelSchema(title=f.channel_title, id=f.channel_id) for f in channel]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@channel_router.post("/channel/")
async def add_channel(channel: ChannelSchema, session: AsyncSession = Depends(get_db)):
    try:
        new_channel = await queri_channel.add_channel(session,
                                                      channel.title,
                                                      channel.synopsis_short,
                                                      channel.synopsis_long,
                                                      channel.keywords,
                                                      channel.audio)
        await session.commit()
        return {"result": new_channel.channel_id}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@channel_router.delete("/channel/{channel_id}/")
async def delete_channel_route(channel_id: int, session: AsyncSession = Depends(get_db)):
    try:
        deleted_channel = await queri_channel.delete_channel(session, channel_id)
        if deleted_channel:
            return {"message": f"Deleted Channel with ID {channel_id}."}
        else:
            raise HTTPException(status_code=404, detail=f"Channel with ID {channel_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@channel_router.post("/op_facade/chnMgmt/AddChannelMapping")
async def add_channel_mapping_endpoint(mapping_data: ChannelMappingSchema, session: AsyncSession = Depends(get_db)):
    try:
        result = await queri_channel.add_channel_mapping(session,
                                                         channelId=mapping_data.channelId,
                                                         targetId=mapping_data.targetId,
                                                         type=mapping_data.type,
                                                         mapped=mapping_data.mapped)
        return result
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))
