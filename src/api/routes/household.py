from typing import Annotated, Any

import anyio
from fastapi import APIRouter, Depends
from operatorfacade.src.zappware.operator_facade.converters import GetAttr
from operatorfacade.src.zappware.operator_facade.enums.media_enums import MediaContentType
from operatorfacade.src.zappware.operator_facade.enums.unlisted import ImgUrls
from operatorfacade.src.zappware.operator_facade.models.client_profile import ClientProfileCustomData
from operatorfacade.src.zappware.operator_facade.models.household import CreateHouseholdResult
from operatorfacade.src.zappware.operator_facade.models.media import MediaData
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from src.api.routes.utils import MobileDatabaseLoader, BASE_DIR
from src.api.services import of
from src.api.services.auth import check_token
from src.api.services.household import HouseholdService, get_household_service
from src.dal.utils import get_db
from src.models.auth import Token
from src.models.household import CreateHouseholdModel, CreateProfileModel, SetUserProfiles, SubscribeProductModel, \
    UnsubscribeProductModel, SetProductStatusModel

household_router = APIRouter(prefix="/households", tags=["households"])
BASE_URL = "http://bil_app-api-1:80/households"


@household_router.post("/create/")
async def create_household(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
        response_data: CreateHouseholdModel,
):
    try:
        hh_ids: CreateHouseholdResult = await of.houshMgmt.create_household_ext(response_data.user,
                                                                                response_data.household,
                                                                                response_data.custom_data,
                                                                                response_data.hashed_password)
        cp_custom = ClientProfileCustomData(active_channel_list="G:1", active_channel="S:1", budget_limit=100000,
                                            language="rus")

        async with await anyio.open_file('.venv/Lib/site-packages/operatorfacade/media/happy_avatar.png', 'rb') as f:
            ava = await f.read()
        data = MediaData(content=ava, content_type=MediaContentType.IMAGE_PNG)

        cpres: int = await of.houshMgmt.create_profile(
            houshId=hh_ids.household_id, name=response_data.user.address, descr='auto create with create household',
            type=1, age=18, pin='1111',
            purchasePin='1111',
            customData=cp_custom,
            images={'': data}
        )

        supres: int = await of.houshMgmt.set_user_profiles(hh_ids.user_id, [cpres], cpres)

    except Exception as e:
        return f"Error: {e}"

    # household = await service.create_household(
    #     session=db_session,
    #     household_data=response_data.household
    # )
    # user = await service.create_user(
    #     session=db_session,
    #     user_data=response_data.user,
    #     household_id=household.id
    # )
    # cp_custom = ClientProfileCustomData(active_channel_list="G:1", active_channel="S:1", budget_limit=100000,
    #                                     language="rus").dict()
    # profile = await service.create_profile(
    #     session=db_session,
    #     profile_data=CreateProfileModel(
    #         household_id=household.id,
    #         name=f"{user.first_name} {user.last_name}",
    #         description='auto create with create household',
    #         type=1,
    #         age=18,
    #         pin='1111',
    #         purchase_pin='1111',
    #         custom_data=json.dumps(cp_custom),
    #     )
    # )
    #
    # user_profiles = await service.set_user_profiles(
    #     session=db_session,
    #     data=SetUserProfiles(
    #         user_id=user.id,
    #         profile_ids=[profile.id],
    #         default_profile_id=profile.id
    #     )
    # )

    return {
        # "user": user,
        # "household": household,
        "response": hh_ids,
        "profile": cpres,
        "set_profile": supres

    }


@household_router.post("/get/")
async def get_household(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
):
    # res = await service.get_household(session=db_session)
    lgpres = await of.houshMgmt.list_households(30, 0, totalCnt=True)
    # for p in lgpres:
    #     ggpres = await of.prodMgmt.get_group_product(p.id)
    #
    # return lgpres
    return {
        # "proxy": res,
        "zappware": lgpres
    }


@household_router.post("/get_household_by_id/")
async def get_household_by_id(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
        household_id: int
):
    # res = await service.get_household_by_id(session=db_session, household_id=household_id)
    res = await of.houshMgmt.get_household(household_id)

    return res


# @household_router.post("/get_household_by_token/")
# async def get_household_by_token(
#         token: Token
# ):
#     username: str | None = await check_token(token.token)
#
#     if username:
#         household_id = int(username.split()[1])
#         res = await of.houshMgmt.get_household(household_id)
#
#         return res
#     return {"result": "ERROR", "message": "User not found"}
#

@household_router.post("/get_household_by_acc_code/")
async def get_household_by_acc_code(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
        acc_code: str
):
    res = await of.houshMgmt.get_household_by_acc_code(acc_code)

    return res


@household_router.post("/get_user_profiles/")
async def get_user_profiles(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
        profile_id: int,
        imgUrls: Annotated[ImgUrls, GetAttr('value')] | None = None
):
    # res = await service.get_user_profiles(session=db_session)
    res = await of.houshMgmt.get_profile(profile_id, imgUrls)
    return res


@household_router.post("/get_user/")
async def get_user(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
        user_id: int
):
    # res = await service.get_user(session=db_session)
    res = await of.houshMgmt.get_user(user_id)
    return res


@household_router.post("/get_user_by_name/")
async def get_user_by_name(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
        username: str
):
    # res = await service.get_user(session=db_session)
    res = await of.houshMgmt.get_user_by_name(username)
    return res


# @household_router.post("/get_user_by_id/")
# async def get_user_by_id(
#         db_session: Annotated[AsyncSession, Depends(get_db)],
#         service: Annotated[HouseholdService, Depends(get_household_service)],
#         user_id: int
# ):
#     res = await service.get_user_by_id(session=db_session, user_id=user_id)
#
#     return res


@household_router.post("/get_products/")
async def get_household_products(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
        household_id: int
):
    # res = await service.get_household_products(session=db_session)
    #
    # return res
    res = await of.houshMgmt.list_household_products(household_id)
    return res


# @household_router.post("/get_products_by_token/")
# async def get_household_products_by_token(
#
#         token: Token
# ):
#     username: str | None = await check_token(token.token)
#
#     if username:
#         household_id = int(username.split()[1])
#
#         res = await of.houshMgmt.list_household_products(household_id)
#         product_ids = [product.product_id for product in res]
#         data = []
#         for product_id in product_ids:
#             product = await of.prodMgmt.get_group_product(product_id)
#             data.append((product.name, product.status))
#
#         return {"result": [{"name": d[0], "status": d[1]} for d in data]}
#     return {"result": "ERROR", "message": "User not found"}
#

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
# @household_router.post("/subscribe_product_by_token/")
# async def subscribe_product_by_token(
#         token: Token,
#         product_name: str
# ):
#     username: str | None = await check_token(token.token)
#     product_id = await name_to_product_id(product_name)
#     if username:
#         household_id = int(username.split()[1])
#
#         res = await of.houshMgmt.list_household_products(household_id)
#         product_ids = set(product.product_id for product in res)
#
#         product_ids.add(product_id)
#         product_ids = list(product_ids)
#         res = await of.houshMgmt.set_household_products(houshId=household_id, productIds=product_ids)
#
#         return res
#     return {"result": "ERROR", "message": "User not found"}
#
#
# @household_router.post("/unsubscribe_product_by_token/")
# async def unsubscribe_product_by_token(
#         token: Token,
#         product_name: str
# ):
#     username: str | None = await check_token(token.token)
#     product_id = await name_to_product_id(product_name)
#     if username:
#         household_id = int(username.split()[1])
#
#         res = await of.houshMgmt.list_household_products(household_id)
#         product_ids = set(product.product_id for product in res)
#
#         product_ids.remove(product_id)
#         product_ids = list(product_ids)
#         res = await of.houshMgmt.set_household_products(houshId=household_id, productIds=product_ids)
#         res = await of.houshMgmt.set_household_product_statuses(houshId=household_id, productIds=list(product_ids), stats=[1*len(product_ids)])
#
#         # res = await of.houshMgmt.set_household_product_statuses(houshId=household_id, productIds=[product_id],
#         #                                                         stats=[0])
#         return res
#     return {"result": "ERROR", "message": "User not found"}
#
#
# @household_router.post("/name_to_product_id/")
# async def name_to_product_id(
#         product_name: str
# ):
#     lgpres = await of.prodMgmt.list_group_products(ImgUrls.CDN, True)
#
#     for product in lgpres:
#         if product.name == product_name:
#             return product.id
#     return {"error": "error"}
#
#
# @household_router.post("/set_product_status_by_token/")
# async def set_product_status_by_token(
#         token: Token,
#         product_ids: list[int],
#         statuses: list[int]
# ):
#     username: str | None = await check_token(token.token)
#
#     if username:
#         household_id = int(username.split()[1])
#         res = await of.houshMgmt.set_household_product_statuses(houshId=household_id, productIds=product_ids,
#                                                                 stats=statuses)
#         return res
#     return {"result": "ERROR", "message": "User not found"}


@household_router.post("/subscribe_product/")
async def subscribe_product(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        service: Annotated[HouseholdService, Depends(get_household_service)],
        subscribe: SubscribeProductModel,
):
    # data = SetProductStatusModel(acc_code=subscribe.acc_code,
    #                              product_id=subscribe.acc_code,
    #                              is_enabled=True, )
    # res = await service.subscribe_product(
    #     session=db_session,
    #     subscribe_data=subscribe
    # )
    # return SubscribeProductModel.model_validate(res)
    res = await of.houshMgmt.set_household_products(houshId=subscribe.household_id, productIds=subscribe.product_ids)
    return res


@household_router.post("/unsubscribe_product/")
async def unsubscribe_product(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
        # unsubscribe: UnsubscribeProductModel,
        household_id: int,
        product_id: int
):
    # data = SetProductStatusModel(household_id=unsubscribe.household_id,
    #                              product_id=unsubscribe.household_id,
    #                              is_enabled=False, )
    # res = await service.set_product_status(
    #     session=db_session,
    #     set_data=data
    # )
    res = await of.houshMgmt.set_household_product_statuses(houshId=household_id, productIds=[product_id], stats=[0])
    return res


@household_router.post("/set_product_status/")
async def set_product_status(
        # db_session: Annotated[AsyncSession, Depends(get_db)],
        # service: Annotated[HouseholdService, Depends(get_household_service)],
        # set_data: SetProductStatusModel,
        household_id: int,
        product_ids: list[int],
        statuses: list[int]
):
    # res = await service.set_product_status(
    #     session=db_session,
    #     set_data=set_data
    # )

    res = await of.houshMgmt.set_household_product_statuses(houshId=household_id, productIds=product_ids,
                                                            stats=statuses)
    return res


# @household_router.get("/billing_url")
# def get_billing_url() -> str:
#     return "https://qr.nspk.ru/AS100001ORTF4GAF80KPJ53K186D9A3G?type=01&bank=100000000007&crc=0C8A"
#
#
# @household_router.get("/color_scheme")
# async def get_color_settings(
#         tenant_id: int,
#         db_session: Annotated[
#             list[dict[str, Any]], Depends(MobileDatabaseLoader("public/assets/settings.json"))
#         ],
# ) -> dict[str, Any]:
#     for settings in db_session:
#         if settings["tenant_id"] == tenant_id:
#             return settings
#     return {"msg": f"Оператор не найден."}
#
#
# @household_router.get("/tenant-logo")
# def get_logo(tenant_id: int) -> FileResponse:
#     return FileResponse(
#         (BASE_DIR.parent / f"public/logo/logo_{tenant_id}.png"), media_type="image/png"
#     )
