from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.channel import Channel, Product, ChannelProduct


async def add_channel(session: AsyncSession, channel_data):
    try:
        new_channel = Channel(**channel_data.dict())
        session.add(new_channel)
        await session.commit()
        return {"response": new_channel.channel_id}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


async def get_channel(session: AsyncSession) -> list[Channel]:
    result = await session.execute(select(Channel))
    return result.scalars().all()


async def set_channel_live_urls(session: AsyncSession, channel_live_urls):
    try:
        channel = await session.execute(
            update(Channel).
            where(channel_live_urls.channel_id == Channel.channel_id).
            values(channel_urls=channel_live_urls.channel_urls)
        )
        await session.commit()
        return {"result": 0}
    except Exception as ex:
        await session.rollback()
        raise ex


async def set_group_product_services(session: AsyncSession, service_ids, product_id):
    try:
        for channel_id in service_ids:
            existing_product_channel = await session.execute(
                select(ChannelProduct).filter_by(product_id=product_id, channel_id=channel_id)
            )
            if existing_product_channel.scalar():
                print(f"ProductChannel already exists for product_id={product_id} and channel_id={channel_id}")
                continue

            new_product_channel = ChannelProduct(product_id=product_id, channel_id=channel_id)
            session.add(new_product_channel)
            print(f"Added new ProductChannel for product_id={product_id} and channel_id={channel_id}")

        await session.commit()
        return {"result": 0}
    except IntegrityError as ex:
        await session.rollback()
        print(f"IntegrityError: {ex}")
        raise ex
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        await session.rollback()
        raise ex


async def add_product(session: AsyncSession, product_data):
    try:
        new_product = Product(**product_data.dict())
        session.add(new_product)
        await session.commit()
        return {"response": new_product.product_id}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


async def get_product_with_channels(session: AsyncSession):
    stmt = select(Product).options(selectinload(Product.channels))
    result = await session.execute(stmt)
    return [t for t in result.scalars().all()]

