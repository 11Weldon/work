from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.sql.ddl import CreateSchema

from src.core.create_app import create_app
from src.dal.utils import engine


# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
#
#     async with engine.begin() as session:
#         await session.execute(CreateSchema("clients_schema", if_not_exists=True))
#         await session.commit()
#         await session.close()
#     yield
#     ...


# app: FastAPI = create_app(lifespan)
app: FastAPI = create_app()