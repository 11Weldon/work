from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services import of
from src.api.services.product import ProductService, get_product_service
from src.dal.utils import get_db
from src.enums.unlisted import ImgUrls
from src.models.product import CreateProductModel, ProductModel
from zappware.operator_facade import OperatorFacade
product_router = APIRouter(prefix="/products", tags=["products"])
BASE_URL = "http://bil_app-api-1:80/products"


@product_router.post("/create/")
async def create_product(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[ProductService, Depends(get_product_service)],
        product: CreateProductModel,
) -> ProductModel:
    res: ProductModel = await service.create_product(
        session=db_session,
        product_data=product
    )
    # async with httpx.AsyncClient() as client:
    #     response = 200
    #     ...
    #     # response = await client.post(f'{BASE_URL}/bundles/get_upsell_info', json=upsell_data.dict())
    return res


@product_router.get("/get/")
async def get_product(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[ProductService, Depends(get_product_service)],
):
    res: ProductModel = await service.get_product(
        session=db_session,
    )
    # lgpres = await of.prodMgmt.list_group_products(ImgUrls.CDN, True)
    # # for p in lgpres:
    # #     ggpres = await of.prodMgmt.get_group_product(p.id)
    # #
    # return lgpres

    return res
