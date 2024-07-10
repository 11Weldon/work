from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.household import UserProfile, Household, Profile, HouseholdProfile, HouseholdProduct


async def create_household(session: AsyncSession, user_data, household_data):
    try:
        new_user = UserProfile(**user_data.dict())
        session.add(new_user)
        await session.flush()

        new_household = Household(**household_data.dict(), user_profile_id=new_user.user_id)
        session.add(new_household)
        await session.commit()
        return {"result id": new_household.household_id}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


async def get_households(session: AsyncSession):
    result = await session.execute(select(Household))
    households = result.scalars().all()
    return households


async def get_users(session: AsyncSession):
    result = await session.execute(select(UserProfile))
    return result.scalars().all()


async def create_profile(session: AsyncSession, profile_data, household_id):
    try:
        new_profile = Profile(**profile_data.dict())
        session.add(new_profile)

        existing_household_profile = await session.execute(
            select(HouseholdProfile).filter_by(household_id=household_id, profile_id=new_profile.profile_id)
        )
        if existing_household_profile.scalar():
            print(f"HouseholdProfile already exists for household_id={household_id} and profile_id={new_profile.profile_id}")

        new_household_profile = HouseholdProfile(household_id=household_id, profile_id=new_profile.profile_id)
        session.add(new_household_profile)

        await session.commit()
        return {"result id": new_profile.profile_id}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


async def get_profiles(session: AsyncSession):
    result = await session.execute(select(Profile))
    return result.scalars().all()


async def set_household_products(session: AsyncSession, profiles_data):
    try:
        for product_id in profiles_data.product_ids:
            existing_household_product = await session.execute(
                select(HouseholdProduct).filter_by(product_id=product_id, household_id=profiles_data.household_id)
            )
            if existing_household_product.scalar():
                print(f"HouseholdProduct already exists for product_id={product_id} and household_id={profiles_data.household_id}")
                continue

            new_household_product = HouseholdProduct(product_id=product_id, household_id=profiles_data.household_id)
            session.add(new_household_product)
            print(f"Added new HouseholdProduct for product_id={product_id} and household_id={profiles_data.household_id}")

        await session.commit()
        return {"result": 0}
    except IntegrityError as ex:
        await session.rollback()
        print(f"IntegrityError: {ex}")
        raise ex
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        await session.rollback()
        raise ex
