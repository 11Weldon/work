from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from database import Base, async_engine, async_session_factory
from models import Client, Bundle, BundleChannel, ClientBundle, Channel
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
    new_func = Channel(channel_id=id, channel_title=title)
    session.add(new_func)
    return new_func


async def get_func(session: AsyncSession) -> list[Channel]:
    result = await session.execute(select(Channel))
    return result.scalars().all()


async def add_bundle(session: AsyncSession, title: str, id: int):
    new_bundle = Bundle(bundle_id=id, bundle_title=title)
    session.add(new_bundle)
    return new_bundle


async def get_bundle(session: AsyncSession) -> list[Bundle]:
    result = await session.execute(select(Bundle))
    return result.scalars().all()


async def add_channel_to_bundle(session: AsyncSession, bundle_id: int, channel_id: int):
    try:
        existing_bundle_channel = await session.execute(
            select(BundleChannel).filter_by(bundle_id=bundle_id, channel_id=channel_id)
        )
        if existing_bundle_channel.scalar():
            print(f"BundleChannel already exists for bundle_id={bundle_id} and channel_id={channel_id}")
            return None

        new_bundle_channel = BundleChannel(bundle_id=bundle_id, channel_id=channel_id)
        session.add(new_bundle_channel)
        await session.commit()
        print(f"Added new BundleChannel for bundle_id={bundle_id} and channel_id={channel_id}")
        return new_bundle_channel
    except IntegrityError as ex:
        await session.rollback()
        print(f"IntegrityError: {ex}")
        return None
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        await session.rollback()
        return None


async def add_client_bundle(session: AsyncSession, client_id: int, bundle_id: int):
    try:
        existing_client_bundle = await session.execute(
            select(ClientBundle).filter_by(client_id=client_id, bundle_id=bundle_id)
        )
        if existing_client_bundle.scalar():
            print(f"ClientBundle already exists for client_id={client_id} and bundle_id={bundle_id}")
            return None

        new_client_bundle = ClientBundle(client_id=client_id, bundle_id=bundle_id)
        session.add(new_client_bundle)
        await session.commit()
        print(f"Added new ClientBundle for client_id={client_id} and bundle_id={bundle_id}")
        return new_client_bundle
    except IntegrityError as ex:
        await session.rollback()
        print(f"IntegrityError: {ex}")
        return None
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        await session.rollback()
        return None


async def get_all_bundles_with_channels(session: AsyncSession):
    stmt = select(Bundle).options(selectinload(Bundle.channels))
    result = await session.execute(stmt)
    return [t for t in result.scalars().all()]


async def get_all_client_bundles(session: AsyncSession):
    stmt = select(Client).options(selectinload(Client.client_bundles).selectinload(ClientBundle.bundle))
    result = await session.execute(stmt)
    return [c for c in result.scalars().all()]


async def delete_client(session: AsyncSession, client_id: int):
    try:
        client = await session.execute(select(Client).filter_by(client_id=client_id))
        client_obj = client.scalar()
        if not client_obj:
            print(f"Client with ID {client_id} not found.")
            return None

        await session.execute(delete(ClientBundle).where(ClientBundle.client_id == client_id))

        await session.delete(client_obj)
        await session.commit()
        print(f"Deleted Client with ID {client_id}.")
        return client_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


async def delete_bundle(session: AsyncSession, bundle_id: int):
    try:
        # Fetch the bundle object
        bundle = await session.execute(select(Bundle).filter_by(bundle_id=bundle_id))
        bundle_obj = bundle.scalar()

        if not bundle_obj:
            print(f"Bundle with ID {bundle_id} not found.")
            return None

        await session.execute(delete(BundleChannel).where(BundleChannel.bundle_id == bundle_id))

        await session.execute(delete(ClientBundle).where(ClientBundle.bundle_id == bundle_id))

        await session.delete(bundle_obj)

        await session.commit()

        print(f"Deleted Bundle with ID {bundle_id}.")
        return bundle_obj
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


async def delete_client_bundle(session: AsyncSession, client_id: int, bundle_id: int):
    try:
        client_bundle = await session.execute(
            select(ClientBundle).filter_by(client_id=client_id, bundle_id=bundle_id)
        )
        client_bundle_obj = client_bundle.scalar()
        if not client_bundle_obj:
            print(f"ClientBundle with client_id={client_id} and bundle_id={bundle_id} not found.")
            return None

        await session.delete(client_bundle_obj)
        await session.commit()
        print(f"Removed Bundle {bundle_id} from Client {client_id}.")
        return client_bundle_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None


async def delete_channel_from_bundle(session: AsyncSession, bundle_id: int, channel_id: int):
    try:
        bundle_channel = await session.execute(
            select(BundleChannel).filter_by(bundle_id=bundle_id, channel_id=channel_id)
        )
        bundle_channel_obj = bundle_channel.scalar()
        if not bundle_channel_obj:
            print(f"BundleChannel with bundle_id={bundle_id} and channel_id={channel_id} not found.")
            return None

        await session.delete(bundle_channel_obj)
        await session.commit()
        print(f"Removed Channel {channel_id} from Bundle {bundle_id}.")
        return bundle_channel_obj
    except Exception as ex:
        await session.rollback()
        print(f"Unexpected error: {ex}")
        return None
