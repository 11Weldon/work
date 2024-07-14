from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.ddl import CreateSchema

from src.dal.schemas import Base
from src.dal.utils import get_db, engine

start_router = APIRouter(prefix="/start", tags=["start"])


@start_router.get("")
async def start(
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    await db_session.execute(CreateSchema("clients_schema", if_not_exists=True))

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"reload": "ok"}
