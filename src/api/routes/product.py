from typing import Annotated

import anyio
from fastapi import APIRouter, Depends
from operatorfacade.src.zappware.operator_facade.enums.media_enums import MediaContentType
from operatorfacade.src.zappware.operator_facade.enums.unlisted import ImgUrls
from operatorfacade.src.zappware.operator_facade.models import GroupProduct

from operatorfacade.src.zappware.operator_facade.models.media import MediaData
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services import of
from src.api.services.product import ProductService, get_product_service
from src.dal.utils import get_db

product_router = APIRouter(prefix="/products", tags=["products"])
# BASE_URL = "http://bil_app-api-1:80/products"


@product_router.post("/create/")
async def create_product(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[ProductService, Depends(get_product_service)],
        product: GroupProduct,
):
    # res = await service.create_product(
    #     session=db_session,
    #     product_data=product
    # )

    aspect = ''
    async with await anyio.open_file('.venv/Lib/site-packages/operatorfacade/media/happy_avatar.png', 'rb') as f:
        ava = await f.read()
    data = MediaData(content=ava, content_type=MediaContentType.IMAGE_PNG)
    images = {aspect: data}

    lgpres = await of.prodMgmt.create_group_product(
            type=product.type,
            externalId=product.external_id,
            status=product.status,
            name=product.name,
            title=product.title,
            descr=product.description,
            custom=product.custom_data,
            prices=product.prices,
            images=images,
            featProdId=product.feat_prod_id)

    return {
        # "proxy": res,
        "zappwer": lgpres,
    }

@product_router.get("/get/")
async def get_product(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[ProductService, Depends(get_product_service)],
):
    # res = await service.get_product(
    #     session=db_session,
    # )
    lgpres = await of.prodMgmt.list_group_products(ImgUrls.CDN, True)

    return {
        # "proxy": res,
        "zappwer": lgpres,
    }
