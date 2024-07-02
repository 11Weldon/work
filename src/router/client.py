from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.queries import queri_client
from src.schema import ClientSchema, ClientWithProductsSchema

clients_router = APIRouter()


@clients_router.get("/client/", response_model=list[ClientSchema])
async def get_cli(session: AsyncSession = Depends(get_db)):
    try:
        clients = await queri_client.get_clients(session)
        return [ClientSchema(name=c.client_name, balance=c.client_balance, id=c.client_id) for c in clients]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@clients_router.get("/clients/", response_model=list[ClientWithProductsSchema])
async def get_all_clients_with_products_route(session: AsyncSession = Depends(get_db)):
    try:
        clients = await queri_client.get_all_client_products(session)
        return [{
            "id": c.client_id,
            "name": c.client_name,
            "balance": c.client_balance,
            "products": [{"id": ct.product.product_id, "title": ct.product.product_title} for ct in c.client_products]
        } for c in clients]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@clients_router.post("/client/")
async def add_cli(client: ClientSchema, session: AsyncSession = Depends(get_db)):
    try:
        client = await queri_client.add_client(session, client.name, client.id, client.balance)
        await session.commit()
        return client
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@clients_router.post("/client/{client_id}/products/{product_id}/")
async def add_client_product(client_id: int, product_id: int, session: AsyncSession = Depends(get_db)):
    try:
        new_client_product = await queri_client.add_client_product(session, client_id, product_id)
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


@clients_router.delete("/client/{client_id}/")
async def delete_client_route(client_id: int, session: AsyncSession = Depends(get_db)):
    try:
        deleted_client = await queri_client.delete_client(session, client_id)
        if deleted_client:
            return {"message": f"Deleted Client with ID {client_id}."}
        else:
            raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@clients_router.delete("/client/{client_id}/products/{product_id}/")
async def delete_client_product_route(client_id: int, product_id: int, session: AsyncSession = Depends(get_db)):
    try:
        removed_client_product = await queri_client.delete_client_product(session, client_id, product_id)
        if removed_client_product:
            return {"message": f"Removed Product {product_id} from Client {client_id}."}
        else:
            raise HTTPException(status_code=404,
                                detail=f"ClientProduct with client_id={client_id} and product_id={product_id} not "
                                       f"found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
