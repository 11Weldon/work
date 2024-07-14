from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.channel import ChannelService, get_channel_service
from src.dal.utils import get_db
from src.models.channel import ListChannelModel, CreateChannel, ChannelModel

channel_router = APIRouter(prefix="/channels", tags=["channels"])


@channel_router.get("")
async def get_channels(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    service: Annotated[ChannelService, Depends(get_channel_service)],
) -> ListChannelModel | None:
    return await service.dal.get_all(db_session=db_session)


@channel_router.post("/create/")
async def create_channel(

    db_session: Annotated[AsyncSession, Depends(get_db)],
    service: Annotated[ChannelService, Depends(get_channel_service)],
    channel: ChannelModel,
) -> ChannelModel:
    res: ChannelModel = await service.add_channel(
        session=db_session,
        channel_data=channel
    )
    if not res:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return ChannelModel.model_validate(res)