from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import get_db
from backend.src.queries.device import add_device
from backend.src.schemas.device import DeviceSchema

device_router = APIRouter()


@device_router.post("/createDevice")
async def create_device_router(device_data: DeviceSchema, session: AsyncSession = Depends(get_db)):
    try:
        new_device = await add_device(session, device_data)
        return new_device
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
