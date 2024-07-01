from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import orm
from schema import ClientSchema, BundleSchema, ChannelSchema, BundleWithChannelsSchema, ClientWithBundlesSchema
from database import get_db


def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    return app


app = create_fastapi_app()


@app.get("/client/", response_model=list[ClientSchema])
async def get_cli(session: AsyncSession = Depends(get_db)):
    try:
        clients = await orm.get_clients(session)
        return [ClientSchema(name=c.client_name, balance=c.client_balance, id=c.client_id) for c in clients]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/bundle/", response_model=list[BundleSchema])
async def get_bundle(session: AsyncSession = Depends(get_db)):
    try:
        bundle = await orm.get_bundle(session)
        return [BundleSchema(title=t.bundle_title, id=t.bundle_id) for t in bundle]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/channel/", response_model=list[ChannelSchema])
async def get_channel(session: AsyncSession = Depends(get_db)):
    try:
        channel = await orm.get_func(session)
        return [ChannelSchema(title=f.channel_title, id=f.channel_id) for f in channel]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/bundles/", response_model=list[BundleWithChannelsSchema])
async def get_all_bundles_with_channels_route(session: AsyncSession = Depends(get_db)):
    try:
        bundles = await orm.get_all_bundles_with_channels(session)
        return [{
            "id": t.bundle_id,
            "title": t.bundle_title,
            "channels": [{"id": f.channel_id, "title": f.channel_title} for f in t.channels]
        } for t in bundles]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clients/", response_model=list[ClientWithBundlesSchema])
async def get_all_clients_with_bundles_route(session: AsyncSession = Depends(get_db)):
    try:
        clients = await orm.get_all_client_bundles(session)
        return [{
            "id": c.client_id,
            "name": c.client_name,
            "balance": c.client_balance,
            "bundles": [{"id": ct.bundle.bundle_id, "title": ct.bundle.bundle_title} for ct in c.client_bundles]
        } for c in clients]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/client/")
async def add_cli(client: ClientSchema, session: AsyncSession = Depends(get_db)):
    try:
        client = await orm.add_client(session, client.name, client.id, client.balance)
        await session.commit()
        return client
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/channel/")
async def add_channel(channel: ChannelSchema, session: AsyncSession = Depends(get_db)):
    try:
        channel = await orm.add_func(session, channel.title, channel.id)
        await session.commit()
        return channel
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/bundle/")
async def add_bundle(bundle: BundleSchema, session: AsyncSession = Depends(get_db)):
    try:
        bundles = await orm.add_bundle(session, bundle.title, bundle.id)
        await session.commit()
        return bundles
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/bundle/{bundle_id}/channel/{channel_id}/")
async def add_channel_to_bundle(bundle_id: int, channel_id: int, session: AsyncSession = Depends(get_db)):
    try:
        new_bundle_channel = await orm.add_channel_to_bundle(session, bundle_id, channel_id)
        await session.commit()
        return new_bundle_channel
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/client/{client_id}/bundles/{bundle_id}/")
async def add_client_bundle(client_id: int, bundle_id: int, session: AsyncSession = Depends(get_db)):
    try:
        new_client_bundle = await orm.add_client_bundle(session, client_id, bundle_id)
        if new_client_bundle:
            return {"message": f"Bundle {bundle_id} added to client {client_id} successfully."}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to add bundle")
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.delete("/client/{client_id}/")
async def delete_client_route(client_id: int, session: AsyncSession = Depends(get_db)):
    try:
        deleted_client = await orm.delete_client(session, client_id)
        if deleted_client:
            return {"message": f"Deleted Client with ID {client_id}."}
        else:
            raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/bundle/{bundle_id}/")
async def delete_bundle_route(bundle_id: int, session: AsyncSession = Depends(get_db)):
    try:
        deleted_bundle = await orm.delete_bundle(session, bundle_id)
        if deleted_bundle:
            return {"message": f"Deleted Bundle with ID {bundle_id}."}
        else:
            raise HTTPException(status_code=404, detail=f"Bundle with ID {bundle_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/channel/{channel_id}/")
async def delete_channel_route(channel_id: int, session: AsyncSession = Depends(get_db)):
    try:
        deleted_channel = await orm.delete_channel(session, channel_id)
        if deleted_channel:
            return {"message": f"Deleted Channel with ID {channel_id}."}
        else:
            raise HTTPException(status_code=404, detail=f"Channel with ID {channel_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/client/{client_id}/bundles/{bundle_id}/")
async def delete_client_bundle_route(client_id: int, bundle_id: int, session: AsyncSession = Depends(get_db)):
    try:
        removed_client_bundle = await orm.delete_client_bundle(session, client_id, bundle_id)
        if removed_client_bundle:
            return {"message": f"Removed Bundle {bundle_id} from Client {client_id}."}
        else:
            raise HTTPException(status_code=404,
                                detail=f"ClientBundle with client_id={client_id} and bundle_id={bundle_id} not "
                                       f"found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/bundle/{bundle_id}/channel/{channel_id}/")
async def delete_channel_from_bundle_route(bundle_id: int, channel_id: int,
                                            session: AsyncSession = Depends(get_db)):
    try:
        removed_channel_from_bundle = await orm.delete_channel_from_bundle(session, bundle_id, channel_id)
        if removed_channel_from_bundle:
            return {"message": f"Removed Channel {channel_id} from Bundle {bundle_id}."}
        else:
            raise HTTPException(status_code=404,
                                detail=f"BundleChannel with bundle_id={bundle_id} and channel_id={channel_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reload/")
async def reload_db():
    await orm.AsyncORM.create_tables()
    return
