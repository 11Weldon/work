import hashlib
from typing import Any
from uuid import uuid4

from ..services import redis_client, of
from ...models.auth import Login


async def check_token(token: str) -> Any:
    return await redis_client.get(token)  # type: ignore


async def delete_token(token: str) -> Any:
    return await redis_client.delete(token)  # type: ignore


def hash_password_sha256(password: str) -> str:
    salt = uuid4().hex
    return (
        hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        + ":"
        + salt
        + ":sha256"
    )


def match_password(hashed: str, password: str) -> bool:
    hashed_password, salt, code = hashed.split(":")
    if code == "sha256":
        if (
            hashed_password
            == hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        ):
            return True
    return False


async def get_authenticate_info(login: Login):

    res = await of.houshMgmt.check_user_pwd(login.username, login.password)
    if res.status == "LOGIN_OK":
        token = str(uuid4())
        account_code = await of.houshMgmt.get_household(res.user.household_id)
        await redis_client.set(token, f"{login.username} {res.user.household_id} {account_code.account_code}")  # type: ignore
        return {"result": "OK", "data": token}
    return {"result": "ERROR", "message": "Something went wrong"}

