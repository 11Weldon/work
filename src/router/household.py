from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.queries import queri_household
from src.schemas.household import CreateHouseholdExtRequest, HouseholdSchema

household_router = APIRouter()


@household_router.post("/op_facade/houshMgmt/CreateHouseholdExt")
async def create_household_ext(request_data: CreateHouseholdExtRequest, session: AsyncSession = Depends(get_db)):
    try:
        result = await queri_household.create_household(session, request_data.user, request_data.household)
        return result
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@household_router.get("/op_facade/houshMgmt/Households/", response_model=list[HouseholdSchema])
async def get_households_route(session: AsyncSession = Depends(get_db)):
    try:
        households = await queri_household.get_households(session)
        return households
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
