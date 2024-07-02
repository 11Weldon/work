from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.models_household import Household, User

from src.schemas.household import UserSchema, HouseholdSchema


async def create_household(session: AsyncSession, user_data: UserSchema, household_data: HouseholdSchema):
    try:
        new_user = User(
            username=user_data.username,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            status=user_data.status,
            address=user_data.address,
            phone=user_data.phone,
            hash_init=user_data.hash_init
        )
        session.add(new_user)
        await session.flush()

        new_household = Household(
            domain=household_data.domain,
            description=household_data.description,
            status=household_data.status,
            accnt_code=household_data.accnt_code,
            locale_id=household_data.locale_id,
            max_devices=household_data.max_devices,
            max_users=household_data.max_users,
            max_profiles=household_data.max_profiles,
            no_pers=household_data.no_pers,
            custom=household_data.custom,
            user_id=new_user.user_id
        )
        session.add(new_household)
        await session.commit()
        return {"result": new_household.household_id}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


async def get_households(session: AsyncSession) -> list[HouseholdSchema]:
    result = await session.execute(select(Household))
    households = result.scalars().all()
    return households
