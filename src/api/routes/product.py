from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.product import ProductService, get_product_service
from src.dal.utils import get_db
from src.models.product import CreateProductModel, ProductModel

product_router = APIRouter(prefix="/products", tags=["products"])
BASE_URL = "http://proxy-api_chtuka-1:81/products"


@product_router.post("/create/")
async def create_product(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[ProductService, Depends(get_product_service)],
        product: CreateProductModel,
):
    res: ProductModel = await service.create_product(
        session=db_session,
        product_data=product
    )
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{BASE_URL}/create/', json=product.dict())

    # return response, response.status_code

    return {"api": ProductModel.model_validate(res),
            "status_code": response.status_code}


@product_router.get("/get/")
async def get_product(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[ProductService, Depends(get_product_service)],
):
    res: ProductModel = await service.get_product(
        session=db_session,
    )
    return res
