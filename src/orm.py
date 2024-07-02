from typing import Dict, Optional, List

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from database import Base, async_engine, async_session_factory
from models import Client, Product, ProductChannel, ClientProduct, Channel, Domain, ChannelMapping
from sqlalchemy.ext.asyncio import AsyncSession


class AsyncORM:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


async def add_client(session: AsyncSession, name: str, id: int, balance: int):
    new_client = Client(client_id=id, client_name=name, client_balance=balance)
    session.add(new_client)
    return new_client


async def get_clients(session: AsyncSession) -> list[Client]:
    result = await session.execute(select(Client))
    return result.scalars().all()


# async def add_сhannel(session: AsyncSession, title: str, id: int):
#     new_func = Channel(channel_id=id, channel_title=title)
#     session.add(new_func)
#     return new_func
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


async def get_func(session: AsyncSession) -> list[Channel]:
    result = await session.execute(select(Channel))
    return result.scalars().all()


async def add_product(session: AsyncSession, title: str, id: int):
    new_product = Product(product_id=id, product_title=title)
    session.add(new_product)
    return new_product


async def get_product(session: AsyncSession) -> list[Product]:
    result = await session.execute(select(Product))
    return result.scalars().all()


async def add_channel_to_product1(session: AsyncSession, product_id: int, channel_id: int):
    try:
        existing_product_channel = await session.execute(
            select(ProductChannel).filter_by(product_id=product_id, channel_id=channel_id)
        )
        if existing_product_channel.scalar():
            print(f"ProductChannel already exists for product_id={product_id} and channel_id={channel_id}")
            return None

        new_product_channel = ProductChannel(product_id=product_id, channel_id=channel_id)
        session.add(new_product_channel)
        await session.commit()
        print(f"Added new ProductChannel for product_id={product_id} and channel_id={channel_id}")
        return new_product_channel
    except IntegrityError as ex:
        await session.rollback()
        print(f"IntegrityError: {ex}")
        return None
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        await session.rollback()
        return None


async def add_channel_to_product(session: AsyncSession, product_id: int, service_ids: List[int]):
    try:
        for channel_id in service_ids:
            existing_product_channel = await session.execute(
                select(ProductChannel).filter_by(product_id=product_id, channel_id=channel_id)
            )
            if existing_product_channel.scalar():
                print(f"ProductChannel already exists for product_id={product_id} and channel_id={channel_id}")
                continue

            new_product_channel = ProductChannel(product_id=product_id, channel_id=channel_id)
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


async def add_client_product(session: AsyncSession, client_id: int, product_id: int):
    try:
        existing_client_product = await session.execute(
            select(ClientProduct).filter_by(client_id=client_id, product_id=product_id)
        )
        if existing_client_product.scalar():
            print(f"ClientProduct already exists for client_id={client_id} and product_id={product_id}")
            return None

        new_client_product = ClientProduct(client_id=client_id, product_id=product_id)
        session.add(new_client_product)
        await session.commit()
        print(f"Added new ClientProduct for client_id={client_id} and product_id={product_id}")
        return new_client_product
    except IntegrityError as ex:
        await session.rollback()
        print(f"IntegrityError: {ex}")
        return None
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        await session.rollback()
        return None


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


async def get_all_products_with_channels(session: AsyncSession):
    stmt = select(Product).options(selectinload(Product.channels))
    result = await session.execute(stmt)
    return [t for t in result.scalars().all()]


async def get_all_client_products(session: AsyncSession):
    stmt = select(Client).options(selectinload(Client.client_products).selectinload(ClientProduct.product))
    result = await session.execute(stmt)
    return [c for c in result.scalars().all()]


async def delete_client(session: AsyncSession, client_id: int):
    try:
        client = await session.execute(select(Client).filter_by(client_id=client_id))
        client_obj = client.scalar()
        if not client_obj:
            print(f"Client with ID {client_id} not found.")
            return None

        await session.execute(delete(ClientProduct).where(ClientProduct.client_id == client_id))

        await session.delete(client_obj)
        await session.commit()
        print(f"Deleted Client with ID {client_id}.")
        return client_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


async def delete_product(session: AsyncSession, product_id: int):
    try:
        # Fetch the product object
        product = await session.execute(select(Product).filter_by(product_id=product_id))
        product_obj = product.scalar()

        if not product_obj:
            print(f"Product with ID {product_id} not found.")
            return None

        await session.execute(delete(ProductChannel).where(ProductChannel.product_id == product_id))

        await session.execute(delete(ClientProduct).where(ClientProduct.product_id == product_id))

        await session.delete(product_obj)

        await session.commit()

        print(f"Deleted Product with ID {product_id}.")
        return product_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


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


async def delete_client_product(session: AsyncSession, client_id: int, product_id: int):
    try:
        client_product = await session.execute(
            select(ClientProduct).filter_by(client_id=client_id, product_id=product_id)
        )
        client_product_obj = client_product.scalar()
        if not client_product_obj:
            print(f"ClientProduct with client_id={client_id} and product_id={product_id} not found.")
            return None

        await session.delete(client_product_obj)
        await session.commit()
        print(f"Removed Product {product_id} from Client {client_id}.")
        return client_product_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


async def delete_channel_from_product(session: AsyncSession, product_id: int, channel_id: int):
    try:
        product_channel = await session.execute(
            select(ProductChannel).filter_by(product_id=product_id, channel_id=channel_id)
        )
        product_channel_obj = product_channel.scalar()
        if not product_channel_obj:
            print(f"ProductChannel with product_id={product_id} and channel_id={channel_id} not found.")
            return None

        await session.delete(product_channel_obj)
        await session.commit()
        print(f"Removed Channel {channel_id} from Product {product_id}.")
        return product_channel_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


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
