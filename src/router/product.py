from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.queries import queri_product
from src.schema import ProductSchema, ProductWithChannelsSchema, ServiceIdsSchema

products_router = APIRouter()


@products_router.get("/product/", response_model=list[ProductSchema])
async def get_product(session: AsyncSession = Depends(get_db)):
    try:
        product = await queri_product.get_product(session)
        return [ProductSchema(title=t.product_title, id=t.product_id) for t in product]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@products_router.get("/products/", response_model=list[ProductWithChannelsSchema])
async def get_all_products_with_channels_route(session: AsyncSession = Depends(get_db)):
    try:
        products = await queri_product.get_all_products_with_channels(session)
        return [{
            "id": t.product_id,
            "title": t.product_title,
            "channels": [{"id": f.channel_id, "title": f.channel_title} for f in t.channels]
        } for t in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@products_router.post("/product/")
async def add_product(product: ProductSchema, session: AsyncSession = Depends(get_db)):
    try:
        products = await queri_product.add_product(session, product.title, product.id)
        await session.commit()
        return products
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@products_router.post("/product/{product_id}/channel/{channel_id}/")
async def add_channel_to_product(product_id: int, channel_id: int, session: AsyncSession = Depends(get_db)):
    try:
        new_product_channel = await queri_product.add_channel_to_product1(session, product_id, channel_id)
        await session.commit()
        return new_product_channel
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@products_router.delete("/product/{product_id}/")
async def delete_product_route(product_id: int, session: AsyncSession = Depends(get_db)):
    try:
        deleted_product = await queri_product.delete_product(session, product_id)
        if deleted_product:
            return {"message": f"Deleted Product with ID {product_id}."}
        else:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@products_router.delete("/product/{product_id}/channel/{channel_id}/")
async def delete_channel_from_product_route(product_id: int, channel_id: int,
                                            session: AsyncSession = Depends(get_db)):
    try:
        removed_channel_from_product = await queri_product.delete_channel_from_product(session, product_id, channel_id)
        if removed_channel_from_product:
            return {"message": f"Removed Channel {channel_id} from Product {product_id}."}
        else:
            raise HTTPException(status_code=404,
                                detail=f"ProductChannel with product_id={product_id} and channel_id={channel_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@products_router.post("/prodMgmt/SetGroupProductServices/{prod_id}")
async def add_services_to_group_product(prod_id: int, service_ids: ServiceIdsSchema,
                                        session: AsyncSession = Depends(get_db)):
    try:
        result = await queri_product.add_channel_to_product(session, prod_id, service_ids.Service_ids)
        return result
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))
