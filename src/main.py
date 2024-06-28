import os
import sys

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import orm
from schema import ClientSchema, TariffSchema, FunctionSchema
from database import get_db


def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Добавьте OPTIONS сюда
        allow_headers=["*"],
    )
    return app


app = create_fastapi_app()


@app.get("/client/", response_model=list[ClientSchema])
async def get_cli(session: AsyncSession = Depends(get_db)):
    try:
        clients = await orm.get_clients(session)
        return [ClientSchema(name=c.client_name, balance=c.client_balance, id=c.client_id) for c in clients]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tariff/", response_model=list[TariffSchema])
async def get_tariff(session: AsyncSession = Depends(get_db)):
    try:
        tariff = await orm.get_tariff(session)
        return [TariffSchema(title=t.tariff_title, id=t.tariff_id) for t in tariff]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tariffs/{tariff_id}/", response_model=list[FunctionSchema])
async def get_tariffs_with_functions_route(tariff_id: int, session: AsyncSession = Depends(get_db)):
    try:
        functions = await orm.get_tariffs_with_functions(session, tariff_id)
        return [FunctionSchema(title=f.function_title, id=f.function_id) for f in functions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/client/{client_id}/tariffs/", response_model=list[TariffSchema])
async def get_client_tariffs_route(client_id: int, session: AsyncSession = Depends(get_db)):
    try:
        tariffs = await orm.get_client_tariffs(session, client_id)
        return [{"id": tariff.tariff_id, "title": tariff.tariff_title} for tariff in tariffs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/function/", response_model=list[FunctionSchema])
async def get_function(session: AsyncSession = Depends(get_db)):
    try:
        function = await orm.get_func(session)
        return [FunctionSchema(title=f.function_title, id=f.function_id) for f in function]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/client/")
async def add_cli(client: ClientSchema, session: AsyncSession = Depends(get_db)):
    try:
        client = await orm.add_client(session, client.name, client.id, client.balance)
        await session.commit()
        return client
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/function/")
async def add_function(function: FunctionSchema, session: AsyncSession = Depends(get_db)):
    try:
        function = await orm.add_func(session, function.title, function.id)
        await session.commit()
        return function
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/tariff/")
async def add_tariff(tariff: TariffSchema, session: AsyncSession = Depends(get_db)):
    try:
        tariffs = await orm.add_tariff(session, tariff.title, tariff.id)
        await session.commit()
        return tariffs
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/tariff/{tariff_id}/function/{function_id}/")
async def add_function_to_tariff(tariff_id: int, function_id: int, session: AsyncSession = Depends(get_db)):
    try:
        new_tariff_function = await orm.add_function_to_tariff(session, tariff_id, function_id)
        await session.commit()
        return new_tariff_function
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/client/{client_id}/tariffs/{tariff_id}/")
async def add_client_tariff(client_id: int, tariff_id: int, session: AsyncSession = Depends(get_db)):
    try:
        new_client_tariff = await orm.add_client_tariff(session, client_id, tariff_id)
        if new_client_tariff:
            return {"message": f"Tariff {tariff_id} added to client {client_id} successfully."}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to add tariff")
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.get("/reload/")
async def reload_db():
    await orm.AsyncORM.create_tables()
    return
