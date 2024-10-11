from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.bundle import BundleService, get_bundle_service
from src.dal.utils import get_db
from src.models.bundle import BundleModel, PurchaiseBundleModel, \
    UpsellBundleRequest
from src.models.product import AddProductToBundle

bundle_router = APIRouter(prefix="/bundles", tags=["bundles"])
BASE_URL = "http://chtuka-api_chtuka-1:81/bundles"


@bundle_router.post("/create/")
async def create_bundle(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[BundleService, Depends(get_bundle_service)],
        bundle: BundleModel,
):
    res = await service.create_bundle(
        session=db_session,
        bundle_data=bundle
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(f'{BASE_URL}/create/', json=bundle.dict())

    return {"api": BundleModel.model_validate(res),
            "status_code": response.status_code}


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


@bundle_router.post("/get/")
async def get_bundles(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[BundleService, Depends(get_bundle_service)],
):
    res = await service.get_bundle(session=db_session, )
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
    res = await service.add_product_to_bundle(
        session=db_session,
        add_data=add_data
    )

    async with httpx.AsyncClient() as client:
        await client.post(f'{BASE_URL}/add_product_to_bundle/', json=add_data.dict())

    return res


@bundle_router.post("/get_upsell_info")
async def get_upsell_info(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[BundleService, Depends(get_bundle_service)],
        upsell_data: UpsellBundleRequest,
):
    res = await service.get_upsell_info(
        session=db_session,
        upsell_info_data=upsell_data,
    )

    return res


@bundle_router.post("/purchaise_bundle")
async def purchaise_bundle(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[BundleService, Depends(get_bundle_service)],
        purchaise_data: PurchaiseBundleModel,
):
    res = await service.purchaise_bundle(
        session=db_session,
        purchaise_data=purchaise_data,
    )

    return res

