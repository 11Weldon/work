from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.utils import BASE_DIR, MobileDatabaseLoader
from src.api.services.auth import check_token, delete_token, get_authenticate_info
from src.api.services.household import HouseholdService, get_household_service
from src.dal.utils import get_db
from src.models.auth import Token, Login

api_authentication = APIRouter(prefix="/authentication", tags=["authentication"])


# @api_authentication.get("/tenant-logo")
# def get_logo(tenant_id: int) -> FileResponse:
#     return FileResponse(
#         (BASE_DIR.parent / f"public/logo/logo_{tenant_id}.png"), media_type="image/png"
#     )


# @api_authentication.post("/subscriber")
# async def get_personal_area(
#         token: Token,
#         db_session: Annotated[
#             list[dict[str, Any]], Depends(MobileDatabaseLoader("public/assets/data.json"))
#         ],
# ) -> dict[str, Any]:
#     username: str | None = check_token(token.token)
#     if username:
#         for user in db_session:
#             if user["username"] == username:
#                 return user
#     return {"result": "ERROR", "message": "User not found"}


# @api_authentication.get("/color_scheme")
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


# @api_authentication.get("/billing_url")
# def get_billing_url() -> str:
#     return "https://qr.nspk.ru/AS100001ORTF4GAF80KPJ53K186D9A3G?type=01&bank=100000000007&crc=0C8A"


# @api_authentication.post("/login")
# async def authentication(
#         login: Login,
# ):
#     res = await get_authenticate_info(
#         login=login
#     )
#     return res


# @api_authentication.post("/subscriptions")
# async def subscriptions(
#         token: Token,
# ):
#     # subscriptions = ["IVI", "AMEDIATEKA", "MEGOGO", "TV_S", "TV_M", "TV_L", "Viju"]
#     username: str | None = check_token(token.token)
#     if username:
#         return
#         # for user in db_session:
#         #     if user["username"] == username:
#         #         return {"result": [{"name": el, "status": el in user["subscriptions"]} for el in subscriptions]}
#     return {"result": "ERROR", "message": "User not found"}


# @api_authentication.post("/logout")
# async def remove_token(token: Token) -> Any:
#     return await delete_token(token=token.token)
#
#
# @api_authentication.get("/token")
# async def token_check(token: Token) -> dict[str, Any]:
#     username = await check_token(token.token)
#     if username:
#         return {"result": "OK", "data": username}
#     return {"result": "ERROR", "message": "Invalid token"}
