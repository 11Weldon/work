import sys
import os

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from database import Base, async_engine, async_session_factory
from models import Client, Function, Tariff, TariffFunction, ClientTariff
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


async def add_func(session: AsyncSession, title: str, id: int):
    new_func = Function(function_id=id, function_title=title)
    session.add(new_func)
    return new_func


async def get_func(session: AsyncSession) -> list[Function]:
    result = await session.execute(select(Function))
    return result.scalars().all()


async def add_tariff(session: AsyncSession, title: str, id: int):
    new_tariff = Tariff(tariff_id=id, tariff_title=title)
    session.add(new_tariff)
    return new_tariff


async def get_tariff(session: AsyncSession) -> list[Tariff]:
    result = await session.execute(select(Tariff))
    return result.scalars().all()


async def add_function_to_tariff(session: AsyncSession, tariff_id: int, function_id: int):
    try:
        existing_tariff_function = await session.execute(
            select(TariffFunction).filter_by(tariff_id=tariff_id, function_id=function_id)
        )
        if existing_tariff_function.scalar():
            print(f"TariffFunction already exists for tariff_id={tariff_id} and function_id={function_id}")
            return None

        new_tariff_function = TariffFunction(tariff_id=tariff_id, function_id=function_id)
        session.add(new_tariff_function)
        await session.commit()
        print(f"Added new TariffFunction for tariff_id={tariff_id} and function_id={function_id}")
        return new_tariff_function
    except IntegrityError as ex:
        await session.rollback()
        print(f"IntegrityError: {ex}")
        return None
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        await session.rollback()
        return None


async def add_client_tariff(session: AsyncSession, client_id: int, tariff_id: int):
    try:
        existing_client_tariff = await session.execute(
            select(ClientTariff).filter_by(client_id=client_id, tariff_id=tariff_id)
        )
        if existing_client_tariff.scalar():
            print(f"ClientTariff already exists for client_id={client_id} and tariff_id={tariff_id}")
            return None

        new_client_tariff = ClientTariff(client_id=client_id, tariff_id=tariff_id)
        session.add(new_client_tariff)
        await session.commit()
        print(f"Added new ClientTariff for client_id={client_id} and tariff_id={tariff_id}")
        return new_client_tariff
    except IntegrityError as ex:
        await session.rollback()
        print(f"IntegrityError: {ex}")
        return None
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        await session.rollback()
        return None


# async def get_tariffs_with_functions(session: AsyncSession, tariff_id: int):
#     stmt = select(Function).join(TariffFunction).join(Tariff).filter(Tariff.tariff_id == tariff_id)
#     result = await session.execute(stmt)
#     return result.scalars().all()
#
#
# async def get_client_tariffs(session: AsyncSession, client_id: int):
#     stmt = select(ClientTariff).options(selectinload(ClientTariff.tariff)).filter_by(client_id=client_id)
#     result = await session.execute(stmt)
#     return [ct.tariff for ct in result.scalars().all()]


async def get_all_tariffs_with_functions(session: AsyncSession):
    stmt = select(Tariff).options(selectinload(Tariff.functions))
    result = await session.execute(stmt)
    return [t for t in result.scalars().all()]


async def get_all_client_tariffs(session: AsyncSession):
    stmt = select(Client).options(selectinload(Client.client_tariffs).selectinload(ClientTariff.tariff))
    result = await session.execute(stmt)
    return [c for c in result.scalars().all()]


async def delete_client(session: AsyncSession, client_id: int):
    try:
        client = await session.execute(select(Client).filter_by(client_id=client_id))
        client_obj = client.scalar()
        if not client_obj:
            print(f"Client with ID {client_id} not found.")
            return None

        # Delete associated ClientTariff records
        await session.execute(delete(ClientTariff).where(ClientTariff.client_id == client_id))

        await session.delete(client_obj)
        await session.commit()
        print(f"Deleted Client with ID {client_id}.")
        return client_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


async def delete_tariff(session: AsyncSession, tariff_id: int):
    try:
        # Fetch the tariff object
        tariff = await session.execute(select(Tariff).filter_by(tariff_id=tariff_id))
        tariff_obj = tariff.scalar()

        if not tariff_obj:
            print(f"Tariff with ID {tariff_id} not found.")
            return None

        # Delete associated TariffFunction records
        await session.execute(delete(TariffFunction).where(TariffFunction.tariff_id == tariff_id))

        # Delete associated ClientTariff records
        await session.execute(delete(ClientTariff).where(ClientTariff.tariff_id == tariff_id))

        # Delete the tariff object itself
        await session.delete(tariff_obj)

        # Commit the transaction
        await session.commit()

        print(f"Deleted Tariff with ID {tariff_id}.")
        return tariff_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


async def delete_function(session: AsyncSession, function_id: int):
    try:
        function = await session.execute(select(Function).filter_by(function_id=function_id))
        function_obj = function.scalar()
        if not function_obj:
            print(f"Function with ID {function_id} not found.")
            return None

        await session.delete(function_obj)
        await session.commit()
        print(f"Deleted Function with ID {function_id}.")
        return function_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


async def remove_client_tariff(session: AsyncSession, client_id: int, tariff_id: int):
    try:
        client_tariff = await session.execute(
            select(ClientTariff).filter_by(client_id=client_id, tariff_id=tariff_id)
        )
        client_tariff_obj = client_tariff.scalar()
        if not client_tariff_obj:
            print(f"ClientTariff with client_id={client_id} and tariff_id={tariff_id} not found.")
            return None

        await session.delete(client_tariff_obj)
        await session.commit()
        print(f"Removed Tariff {tariff_id} from Client {client_id}.")
        return client_tariff_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


async def remove_function_from_tariff(session: AsyncSession, tariff_id: int, function_id: int):
    try:
        tariff_function = await session.execute(
            select(TariffFunction).filter_by(tariff_id=tariff_id, function_id=function_id)
        )
        tariff_function_obj = tariff_function.scalar()
        if not tariff_function_obj:
            print(f"TariffFunction with tariff_id={tariff_id} and function_id={function_id} not found.")
            return None

        await session.delete(tariff_function_obj)
        await session.commit()
        print(f"Removed Function {function_id} from Tariff {tariff_id}.")
        return tariff_function_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None
