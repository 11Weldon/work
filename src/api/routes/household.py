import json
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.household import HouseholdService, get_household_service
from src.dal.utils import get_db
from src.models.household import CreateHouseholdModel, CreateProfileModel, ClientProfileCustomData, SetUserProfiles

household_router = APIRouter(prefix="/households", tags=["households"])

BASE_URL = "http://chtuka-api_chtuka-1:81/households"


@household_router.post("/create/")
async def create_household(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
        response_data: CreateHouseholdModel,
):
    response_dict = response_data.dict()
    # return response_dict
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{BASE_URL}/create/', json=response_dict)

    if response.status_code == 200:
    # if True:
        household = await service.create_household(
            session=db_session,
            household_data=response_data.household
        )
        user = await service.create_user(
            session=db_session,
            user_data=response_data.user,
            household_id=household.id
        )
        cp_custom = ClientProfileCustomData(active_channel_list="G:1", active_channel="S:1", budget_limit=100000, language="rus").dict()
        profile = await service.create_profile(
            session=db_session,
            profile_data=CreateProfileModel(
                household_id=household.id,
                name=f"{user.first_name} {user.last_name}",
                description='auto create with create household',
                type=1,
                age=18,
                pin='1111',
                purchase_pin='1111',
                custom_data=json.dumps(cp_custom),
            )
        )

        user_profiles = await service.set_user_profiles(
            session=db_session,
            data=SetUserProfiles(
                user_id=user.id,
                profile_ids=[profile.id],
                default_profile_id=profile.id
            )
        )

        return {
            "user": user,
            "household": household,
            "profile": profile,
            "user_profiles": user_profiles,
            "response": response.json()

        }
    return response.json()


@household_router.post("/get/")
async def get_household(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
):
    res = await service.get_household(session=db_session)

    return res


@household_router.post("/get_user_profiles/")
async def get_user_profiles(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
):
    res = await service.get_user_profiles(session=db_session)

    return res


@household_router.post("/get_user/")
async def get_user(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
):
    res = await service.get_user(session=db_session)

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
