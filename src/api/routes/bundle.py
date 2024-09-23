from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services import of
from src.api.services.bundle import BundleService, get_bundle_service
from src.dal.utils import get_db
from src.enums.unlisted import ImgUrls
from src.models.bundle import BundleModel, UpsellInfoModel, AddBundleToUpsell, GetUpsellInfoModel, PurchaiseBundleModel, \
    UpsellBundleRequest
from src.models.product import AddProductToBundle

# BASE_URL = 'http://localhost:80/'

bundle_router = APIRouter(prefix="/bundles", tags=["bundles"])
BASE_URL = "http://bil_app-api-1:80/bundles"


@bundle_router.post("/create/")
async def create_bundle(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[BundleService, Depends(get_bundle_service)],
        bundle: BundleModel,
):
    # async with httpx.AsyncClient() as client:
    #     response = 200
    #     ...
    #     # response = await client.post(f'{BASE_URL}/bundles/get_upsell_info', json=upsell_data.dict())

    res = await service.create_bundle(
        session=db_session,
        bundle_data=bundle
    )
    return res


# @bundle_router.post("/create/upsell_info")
# async def create_upsell_info(
#         db_session: Annotated[AsyncSession, Depends(get_db)],
#         service: Annotated[BundleService, Depends(get_bundle_service)],
#         upsell: UpsellInfoModel,
# ):
#     res = await service.create_upsell_info(
#         session=db_session,
#         upsell_info_data=upsell
#     )
#     return UpsellInfoModel.model_validate(res)

# #
@bundle_router.post("/get/")
async def get_bundles(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[BundleService, Depends(get_bundle_service)],
):
    res = await service.get_bundle(session=db_session, )
    # lgpres = await of.prodMgmt.list_bundles(ImgUrls.CDN, True)
    # # for p in lgpres:
    # #     ggpres = await of.prodMgmt.get_group_product(p.id)
    # #
    # return lgpres
    return res


# @bundle_router.post("/add_bundle_to_upsell")
# async def add_bundle_to_upsell(
#         db_session: Annotated[AsyncSession, Depends(get_db)],
#         service: Annotated[BundleService, Depends(get_bundle_service)],
#         upsell_data: AddBundleToUpsell,
# ):
#     res = await service.add_bundle_to_upsell(
#         session=db_session,
#         bundle_data=upsell_data
#     )
#     return res


@bundle_router.post("/add_product_to_bundle")
async def add_product_to_bundle(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[BundleService, Depends(get_bundle_service)],
        add_data: AddProductToBundle,
):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{BASE_URL}/add_product_to_bundle', json=add_data.json())

    if response == 200:

        res = await service.add_product_to_bundle(
            session=db_session,
            add_data=add_data
        )
        return res
    else:
        return


@bundle_router.post("/get_upsell_info")
async def get_upsell_info(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[BundleService, Depends(get_bundle_service)],
        upsell_data: UpsellBundleRequest,
):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{BASE_URL}/get_upsell_info', json=upsell_data.dict())

    return response


@bundle_router.post("/purchaise_bundle")
async def purchaise_bundle(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[BundleService, Depends(get_bundle_service)],
        purchaise_data: PurchaiseBundleModel,
):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{BASE_URL}/purchaise_bundle', json=purchaise_data.dict())

    return response

