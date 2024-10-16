from typing import Annotated, Any

from fastapi import APIRouter, Depends
from operatorfacade.src.zappware.operator_facade.enums import ImgUrls
from starlette.responses import FileResponse

from src.api.routes.utils import MobileDatabaseLoader, BASE_DIR
from src.api.services import of, redis_client
from src.api.services.auth import check_token, get_authenticate_info, delete_token
from src.models.auth import Token, Login, Product

api_backend_router = APIRouter(prefix="/lenabackend/api", tags=["api"])


@api_backend_router.post("/get_household_by_token/")
async def get_household_by_token(
        token: Token
):
    username: str | None = await check_token(token.token)

    if username:
        household_id = int(username.split()[1])
        res = await of.houshMgmt.get_household(household_id)

        return res
    return {"result": "ERROR", "message": "User not found"}


@api_backend_router.post("/get_products_by_token/")
async def get_household_products_by_token(

        token: Token
):
    username: str | None = await check_token(token.token)

    if username:
        household_id = int(username.split()[1])

        res = await of.houshMgmt.list_household_products(household_id)
        product_ids = [product.product_id for product in res]
        data = []
        for product_id in product_ids:
            product = await of.prodMgmt.get_group_product(product_id)
            data.append((product.name, product.status))

        return {"result": [{"name": d[0], "status": d[1]} for d in data]}
    return {"result": "ERROR", "message": "User not found"}


@api_backend_router.post("/subscribe_product_by_token/")
async def subscribe_product_by_token(
        token: Token,
        product_name: str
):
    username: str | None = await check_token(token.token)
    product_id = await name_to_product_id(product_name)
    if username:
        household_id = int(username.split()[1])

        res = await of.houshMgmt.list_household_products(household_id)
        product_ids = set(product.product_id for product in res)

        product_ids.add(product_id)
        product_ids = list(product_ids)
        res = await of.houshMgmt.set_household_products(houshId=household_id, productIds=product_ids)

        return res
    return {"result": "ERROR", "message": "User not found"}


@api_backend_router.post("/unsubscribe_product_by_token/")
async def unsubscribe_product_by_token(
        token: Token,
        product_name: str
):
    username: str | None = await check_token(token.token)
    product_id = await name_to_product_id(product_name)
    if username:
        household_id = int(username.split()[1])

        res = await of.houshMgmt.list_household_products(household_id)
        product_ids = set(product.product_id for product in res)

        product_ids.remove(product_id)
        product_ids = list(product_ids)
        res = await of.houshMgmt.set_household_products(houshId=household_id, productIds=product_ids)
        res = await of.houshMgmt.set_household_product_statuses(houshId=household_id, productIds=list(product_ids),
                                                                stats=[1 * len(product_ids)])

        # res = await of.houshMgmt.set_household_product_statuses(houshId=household_id, productIds=[product_id],
        #                                                         stats=[0])
        return res
    return {"result": "ERROR", "message": "User not found"}


@api_backend_router.post("/name_to_product_id/")
async def name_to_product_id(
        product_name: str
):
    cached_products = await redis_client.get("all_products")

    if cached_products is None:
        lgpres = await of.prodMgmt.list_group_products(ImgUrls.CDN, True)
        products = [Product(name=product.name, id=product.id) for product in lgpres]
        await redis_client.set("all_products", str(products), ex=86400)
    else:
        lgpres = eval(cached_products)

    for product in lgpres:
        if product.name == product_name:
            return product.id
    return {"error": "Product not found"}


@api_backend_router.post("/set_product_status_by_token/")
async def set_product_status_by_token(
        token: Token,
        product_ids: list[int],
        statuses: list[int]
):
    username: str | None = await check_token(token.token)

    if username:
        household_id = int(username.split()[1])
        res = await of.houshMgmt.set_household_product_statuses(houshId=household_id, productIds=product_ids,
                                                                stats=statuses)
        return res
    return {"result": "ERROR", "message": "User not found"}


@api_backend_router.get("/billing_url")
def get_billing_url() -> str:
    return "https://qr.nspk.ru/AS100001ORTF4GAF80KPJ53K186D9A3G?type=01&bank=100000000007&crc=0C8A"


@api_backend_router.get("/color_scheme")
async def get_color_settings(
        tenant_id: int,
        db_session: Annotated[
            list[dict[str, Any]], Depends(MobileDatabaseLoader("public/assets/settings.json"))
        ],
) -> dict[str, Any]:
    for settings in db_session:
        if settings["tenant_id"] == tenant_id:
            return settings
    return {"msg": f"Оператор не найден."}


@api_backend_router.get("/tenant-logo")
def get_logo(tenant_id: int) -> FileResponse:
    return FileResponse(
        (BASE_DIR.parent / f"public/logo/logo_{tenant_id}.png"), media_type="image/png"
    )


@api_backend_router.post("/login")
async def authentication(
        login: Login,
):
    res = await get_authenticate_info(
        login=login
    )
    return res


@api_backend_router.post("/logout")
async def remove_token(token: Token) -> Any:
    return await delete_token(token=token.token)


@api_backend_router.get("/token")
async def token_check(token: Token) -> dict[str, Any]:
    username = await check_token(token.token)
    if username:
        return {"result": "OK", "data": username}
    return {"result": "ERROR", "message": "Invalid token"}
