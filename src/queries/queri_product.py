from typing import List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Product, ProductChannel, ClientProduct


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


async def get_all_products_with_channels(session: AsyncSession):
    stmt = select(Product).options(selectinload(Product.channels))
    result = await session.execute(stmt)
    return [t for t in result.scalars().all()]


async def delete_product(session: AsyncSession, product_id: int):
    try:
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
