from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from sqlalchemy.sql.ddl import CreateSchema
from starlette.responses import JSONResponse

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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="This is a very cool project",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return JSONResponse(custom_openapi())


app.openapi = custom_openapi