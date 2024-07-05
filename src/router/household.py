from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.queries import household
from src.schemas.household import HouseholdSchema, UserSchema, ProfileSchema, HouseholdProducts

household_router = APIRouter()


@household_router.post("/op_facade/houshMgmt/CreateHouseholdExt")
async def create_household_ext(household_data: HouseholdSchema, user_data: UserSchema,
                               session: AsyncSession = Depends(get_db)):
    try:
        new_household = await household.create_household(session, user_data, household_data)
        await session.commit()
        return {"message": f"Household created successfully {new_household=}"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create household: {str(e)}")


@household_router.get("/op_facade/houshMgmt/Households/", response_model=list[HouseholdSchema])
async def get_households_route(session: AsyncSession = Depends(get_db)):
    try:
        households = await household.get_households(session)
        return households
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@household_router.get("/op_facade/houshMgmt/Users/", response_model=list[UserSchema])
async def get_users_route(session: AsyncSession = Depends(get_db)):
    try:
        users = await household.get_users(session)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@household_router.post("/op_facade/houshMgmt/CreateProfile")
async def create_profile_route(household_id: int, profile_data: ProfileSchema,
                               session: AsyncSession = Depends(get_db)):
    try:
        new_household = await household.create_profile(session, profile_data, household_id)
        await session.commit()
        return {"message": f"Profile created successfully {new_household=}"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create household: {str(e)}")


@household_router.get("/op_facade/houshMgmt/Profiles/", response_model=list[ProfileSchema])
async def get_profiles_route(session: AsyncSession = Depends(get_db)):
    try:
        profiles = await household.get_profiles(session)
        return profiles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @household_router.post("/op_facade/houshMgmt/CreateProfile")
# async def create_profile_and_set_household_products_route(profiles_data: HouseholdProducts,
#                                                           session: AsyncSession = Depends(get_db)):
#     try:
#         new_household_products = await household.set_household_products(session, profiles_data)
#         await session.commit()
#         return {"message": f"Profiles added successfully {new_household_products=}"}
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail=f"Failed to create household: {str(e)}")


@household_router.post("/op_facade/prodMgmt/SetHouseholdProds")
async def set_group_product_services_route(
        household_products: HouseholdProducts,
        session: AsyncSession = Depends(get_db)
):
    try:
        new_household_products = await household.set_household_products(session, household_products)
        return new_household_products
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))
