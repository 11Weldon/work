from typing import Annotated

import anyio
from fastapi import APIRouter, Depends
from operatorfacade.src.zappware.operator_facade.enums.media_enums import MediaContentType
from operatorfacade.src.zappware.operator_facade.models.client_profile import ClientProfileCustomData
from operatorfacade.src.zappware.operator_facade.models.household import CreateHouseholdResult
from operatorfacade.src.zappware.operator_facade.models.media import MediaData
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services import of
from src.api.services.household import HouseholdService, get_household_service
from src.dal.utils import get_db
from src.models.household import CreateHouseholdModel

household_router = APIRouter(prefix="/households", tags=["households"])
BASE_URL = "http://bil_app-api-1:80/households"


@household_router.post("/create/")
async def create_household(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
        response_data: CreateHouseholdModel,
):
    try:
        hh_ids: CreateHouseholdResult = await of.houshMgmt.create_household_ext(response_data.user,
                                                                                response_data.household,
                                                                                response_data.custom_data,
                                                                                response_data.hashed_password)
        cp_custom = ClientProfileCustomData(active_channel_list="G:1", active_channel="S:1", budget_limit=100000,
                                            language="rus")
        aspect = ''
        async with await anyio.open_file('.venv/Lib/site-packages/operatorfacade/media/happy_avatar.png', 'rb') as f:
            ava = await f.read()
        data = MediaData(content=ava, content_type=MediaContentType.IMAGE_PNG)

        cpres: int = await of.houshMgmt.create_profile(
            houshId=hh_ids.household_id, name=response_data.user.address, descr='auto create with create household', type=1, age=18, pin='1111',
            purchasePin='1111',
            customData=cp_custom,
            images={aspect: data}
        )

        supres: int = await of.houshMgmt.set_user_profiles(hh_ids.user_id, [cpres], cpres)

    except Exception as e:
        return f"Error: {e}"

    household = await service.create_household(
        session=db_session,
        household_data=response_data.household
    )
    user = await service.create_user(
        session=db_session,
        user_data=response_data.user
    )

    return {
        "user": user,
        "household": household,
        "response": hh_ids,
        "profile": cpres,
        "set_profile": supres

    }


@household_router.post("/get/")
async def get_household(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
):
    res = await service.get_household(session=db_session)
    lgpres = await of.houshMgmt.list_households(30, 0, totalCnt=True)
    # for p in lgpres:
    #     ggpres = await of.prodMgmt.get_group_product(p.id)
    #
    # return lgpres
    return {"proxy": res,
            "zappware": lgpres
            }

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
