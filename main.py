from typing import Optional, Dict

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.device import Device
from src.queries.orm import AsyncORM
from src.router import channel, household, product


def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    return app


app = create_fastapi_app()

app.include_router(channel.channel_router)
app.include_router(household.household_router)
app.include_router(product.product_router)


class DeviceSchema(BaseModel):
    external_id: str
    descr: str
    name: Optional[Dict[str, str]] = Field(default_factory=dict)


async def add_channel(session: AsyncSession, device_data):
    try:
        new_device = Device(**device_data.dict())
        session.add(new_device)
        await session.commit()
        return {"response": new_device.device_id}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/createDevice")
async def create_device_router(device_data: DeviceSchema, session: AsyncSession = Depends(get_db)):
    try:
        new_device = await add_channel(session, device_data)
        return new_device
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.get("/reload/")
async def reload_db():
    await AsyncORM.create_tables()
    return
