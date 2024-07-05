from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.queries import channel
from src.schemas.channel import ChannelSchema, ChannelLiveUrlsSchema, SetGroupProductServicesRequest, ProductSchema


channel_router = APIRouter()


@channel_router.post("/op_facade/chnMgmt/CreateChannel")
async def create_channel(channel_data: ChannelSchema,
                         session: AsyncSession = Depends(get_db)
                         ):
    try:
        new_channel = await channel.add_channel(session, channel_data)
        return new_channel
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@channel_router.get("/op_facade/chnMgmt/Channels")
async def get_channels(session: AsyncSession = Depends(get_db)):
    try:
        channels = await channel.get_channel(session)
        return channels
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@channel_router.post("/op_facade/chnMgmt/SetChannelLiveUrls")
async def set_channel_live_urls_route(channel_live_urls: ChannelLiveUrlsSchema,
                                      session: AsyncSession = Depends(get_db)
                                      ):
    try:
        await channel.set_channel_live_urls(session, channel_live_urls)
        return {"result": 0}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@channel_router.post("/op_facade/prodMgmt/SetGroupProductServices")
async def set_group_product_services_route(
        group_product_services: SetGroupProductServicesRequest,
        session: AsyncSession = Depends(get_db)
):
    try:
        result = await channel.set_group_product_services(session, group_product_services.service_ids, group_product_services.product_id)
        return result
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@channel_router.post("/op_facade/chnMgmt/CreateProduct")
async def create_product(product_data: ProductSchema,
                         session: AsyncSession = Depends(get_db)
                         ):
    try:
        new_product = await channel.add_product(session, product_data)
        return new_product
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@channel_router.get("/op_facade/prodMgmt/ProductsWithChannels")
async def get_product_with_channels_route(session: AsyncSession = Depends(get_db)):
    try:
        product_with_channels = await channel.get_product_with_channels(session)
        if not product_with_channels:
            raise HTTPException(status_code=404, detail=f"Product  not found")

        return product_with_channels

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))