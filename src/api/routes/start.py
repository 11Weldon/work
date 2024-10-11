from fastapi import APIRouter

from src.dal.schemas import Base
from src.dal.utils import engine

start_router = APIRouter(prefix="/start", tags=["start"])


@start_router.get("")
async def start():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all(checkfirst=True))
        await conn.run_sync(Base.metadata.create_all)

    return {"reload": "ok"}