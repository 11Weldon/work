from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.models import Client, ClientProduct


async def add_client(session: AsyncSession, name: str, id: int, balance: int):
    new_client = Client(client_id=id, client_name=name, client_balance=balance)
    session.add(new_client)
    return new_client


async def get_clients(session: AsyncSession) -> list[Client]:
    result = await session.execute(select(Client))
    return result.scalars().all()


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
