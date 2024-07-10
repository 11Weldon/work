from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.device import Device


async def add_device(session: AsyncSession, device_data):
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
