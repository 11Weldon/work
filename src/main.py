from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import orm
from schema import ClientSchema, ProductSchema, ChannelSchema, ProductWithChannelsSchema, ClientWithProductsSchema, \
    ServiceIdsSchema, DomainSchema, ChannelMappingSchema
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


@app.get("/product/", response_model=list[ProductSchema])
async def get_product(session: AsyncSession = Depends(get_db)):
    try:
        product = await orm.get_product(session)
        return [ProductSchema(title=t.product_title, id=t.product_id) for t in product]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/channel/", response_model=list[ChannelSchema])
async def get_channel(session: AsyncSession = Depends(get_db)):
    try:
        channel = await orm.get_func(session)
        return [ChannelSchema(title=f.channel_title, id=f.channel_id) for f in channel]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/", response_model=list[ProductWithChannelsSchema])
async def get_all_products_with_channels_route(session: AsyncSession = Depends(get_db)):
    try:
        products = await orm.get_all_products_with_channels(session)
        return [{
            "id": t.product_id,
            "title": t.product_title,
            "channels": [{"id": f.channel_id, "title": f.channel_title} for f in t.channels]
        } for t in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clients/", response_model=list[ClientWithProductsSchema])
async def get_all_clients_with_products_route(session: AsyncSession = Depends(get_db)):
    try:
        clients = await orm.get_all_client_products(session)
        return [{
            "id": c.client_id,
            "name": c.client_name,
            "balance": c.client_balance,
            "products": [{"id": ct.product.product_id, "title": ct.product.product_title} for ct in c.client_products]
        } for c in clients]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/op_facade/chnMgmt/AddChannelMapping")
async def add_channel_mapping_endpoint(mapping_data: ChannelMappingSchema, session: AsyncSession = Depends(get_db)):
    try:
        result = await orm.add_channel_mapping(session,
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
        new_channel = await orm.add_channel(session,
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


@app.post("/product/")
async def add_product(product: ProductSchema, session: AsyncSession = Depends(get_db)):
    try:
        products = await orm.add_product(session, product.title, product.id)
        await session.commit()
        return products
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/product/{product_id}/channel/{channel_id}/")
async def add_channel_to_product(product_id: int, channel_id: int, session: AsyncSession = Depends(get_db)):
    try:
        new_product_channel = await orm.add_channel_to_product1(session, product_id, channel_id)
        await session.commit()
        return new_product_channel
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/prodMgmt/SetGroupProductServices/{prod_id}")
async def add_services_to_group_product(prod_id: int, service_ids: ServiceIdsSchema,
                                        session: AsyncSession = Depends(get_db)):
    try:
        result = await orm.add_channel_to_product(session, prod_id, service_ids.Service_ids)
        return result
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/op_facade/domMgmt/CreateDomain")
async def create_domain(domain_data: DomainSchema, session: AsyncSession = Depends(get_db)):
    try:

        new_domain = await orm.create_domain(session, domain_data.title, domain_data.descr)
        return {"message": f"Domain {new_domain.title} created successfully."}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/client/{client_id}/products/{product_id}/")
async def add_client_product(client_id: int, product_id: int, session: AsyncSession = Depends(get_db)):
    try:
        new_client_product = await orm.add_client_product(session, client_id, product_id)
        if new_client_product:
            return {"message": f"Product {product_id} added to client {client_id} successfully."}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to add product")
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


@app.delete("/product/{product_id}/")
async def delete_product_route(product_id: int, session: AsyncSession = Depends(get_db)):
    try:
        deleted_product = await orm.delete_product(session, product_id)
        if deleted_product:
            return {"message": f"Deleted Product with ID {product_id}."}
        else:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
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


@app.delete("/client/{client_id}/products/{product_id}/")
async def delete_client_product_route(client_id: int, product_id: int, session: AsyncSession = Depends(get_db)):
    try:
        removed_client_product = await orm.delete_client_product(session, client_id, product_id)
        if removed_client_product:
            return {"message": f"Removed Product {product_id} from Client {client_id}."}
        else:
            raise HTTPException(status_code=404,
                                detail=f"ClientProduct with client_id={client_id} and product_id={product_id} not "
                                       f"found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/product/{product_id}/channel/{channel_id}/")
async def delete_channel_from_product_route(product_id: int, channel_id: int,
                                           session: AsyncSession = Depends(get_db)):
    try:
        removed_channel_from_product = await orm.delete_channel_from_product(session, product_id, channel_id)
        if removed_channel_from_product:
            return {"message": f"Removed Channel {channel_id} from Product {product_id}."}
        else:
            raise HTTPException(status_code=404,
                                detail=f"ProductChannel with product_id={product_id} and channel_id={channel_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reload/")
async def reload_db():
    await orm.AsyncORM.create_tables()
    return
