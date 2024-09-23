from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.household import HouseholdService, get_household_service
from src.dal.utils import get_db
from src.models.household import CreateHouseholdModel

household_router = APIRouter(prefix="/households", tags=["households"])
BASE_URL = "http://proxy-api_chtuka-1:81/households"


@household_router.post("/create/")
async def create_household(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
        household: CreateHouseholdModel,
):
    res: CreateHouseholdModel = await service.create_household(
        session=db_session,
        household_data=household.household
    )
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{BASE_URL}/create/', json=household.dict())

    return {"api": CreateHouseholdModel.model_validate(res),
            "res": response.status_code}


@household_router.post("/get/")
async def get_household(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
):
    res = await service.get_household(session=db_session)

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
#     # async with httpx.AsyncClient() as client:
#     #     response = await client.post(f'{BASE_URL}/update_household_info/', json=household.dict())
#     return CreateHouseholdModel.model_validate(res)
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
#     # async with httpx.AsyncClient() as client:
#     #     response = await client.post(f'{BASE_URL}/update_household/', json=household.dict())
#     return CreateHouseholdModel.model_validate(res)

#
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
