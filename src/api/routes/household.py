from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services import of
from src.api.services.household import HouseholdService, get_household_service
from src.dal.utils import get_db
from src.enums.unlisted import ImgUrls
from src.models.household import CreateHouseholdModel, UpdateHouseholdInfoModel, UpdateHouseholdModel

household_router = APIRouter(prefix="/households", tags=["households"])
BASE_URL = "http://bil_app-api-1:80/households"


@household_router.post("/create/")
async def create_household(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
        household: CreateHouseholdModel,
) -> CreateHouseholdModel:
    res: CreateHouseholdModel = await service.create_household(
        session=db_session,
        household_data=household.household
    )
    # async with httpx.AsyncClient() as client:
    #     response = 200
    #     ...
    #     # response = await client.post(f'{BASE_URL}/bundles/get_upsell_info', json=upsell_data.dict())
    return res


@household_router.post("/get/")
async def get_household(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
):
    res = await service.get_household(session=db_session)
    # lgpres = await of.prodMgmt.list_group_products(ImgUrls.CDN, True)
    # # for p in lgpres:
    # #     ggpres = await of.prodMgmt.get_group_product(p.id)
    # #
    # return lgpres
    return res


# @household_router.post("/update_household_info/")
# async def update_household_info(
#         db_session: Annotated[AsyncSession, Depends(get_db)],
#         service: Annotated[HouseholdService, Depends(get_household_service)],
#         household: UpdateHouseholdInfoModel,
# ) -> CreateHouseholdModel:
#     res: CreateHouseholdModel = await service.update_household_info(
#         session=db_session,
#         household_data=household
#     )
#     async with httpx.AsyncClient() as client:
#         response = 200
#         ...
#         # response = await client.post(f'{BASE_URL}/bundles/get_upsell_info', json=upsell_data.dict())
#     return response
#
#
# @household_router.post("/update_household/")
# async def update_household(
#         db_session: Annotated[AsyncSession, Depends(get_db)],
#         service: Annotated[HouseholdService, Depends(get_household_service)],
#         household: UpdateHouseholdModel,
# ) -> CreateHouseholdModel:
#     res: CreateHouseholdModel = await service.update_household_info(
#         session=db_session,
#         household_data=household
#     )
#     async with httpx.AsyncClient() as client:
#         response = 200
#         ...
#         # response = await client.post(f'{BASE_URL}/bundles/get_upsell_info', json=upsell_data.dict())
#     return response


# @household_router.post("/subscribe_product/")
# async def subscribe_product(
#         db_session: Annotated[AsyncSession, Depends(get_db)],
#         service: Annotated[HouseholdService, Depends(get_household_service)],
#         subscribe: SubscribeProductModel,
# ) -> SubscribeProductModel:
#     res = await service.subscribe_product(
#         session=db_session,
#         subscribe_data=subscribe
#     )
#     return SubscribeProductModel.model_validate(res)
#
#
# @household_router.post("/unsubscribe_product/")
# async def unsubscribe_product(
#         db_session: Annotated[AsyncSession, Depends(get_db)],
#         service: Annotated[HouseholdService, Depends(get_household_service)],
#         unsubscribe: UnsubscribeProductModel,
# ):
#     res = await service.unsubscribe_product(
#         session=db_session,
#         unsubscribe_data=unsubscribe
#     )
#     return res
#     return UnsubscribeProductModel.model_validate(res)
#
#
# @household_router.post("/set_product_status/")
# async def set_product_status(
#         db_session: Annotated[AsyncSession, Depends(get_db)],
#         service: Annotated[HouseholdService, Depends(get_household_service)],
#         set_data: SetProductStatusModel,
# ) -> SetProductStatusModel:
#     res = await service.set_product_status(
#         session=db_session,
#         set_data=set_data
#     )
#     return SetProductStatusModel.model_validate(res)
