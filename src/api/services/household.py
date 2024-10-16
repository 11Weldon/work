from typing import Union

from operatorfacade.src.zappware.operator_facade.models.household import HouseholdInfo
from operatorfacade.src.zappware.operator_facade.models.user import UserInfo
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.services.auth import hash_password_sha256
from src.dal.schemas.household import HouseholdORM, UserORM, UserProfilesORM, ClientProfileORM
from src.dal.schemas.product import HouseholdToProductORM
from src.models.household import UpdateHouseholdInfoModel, UpdateHouseholdModel, HouseholdEntity, SetUserProfiles, \
    CreateProfileModel, UnsubscribeProductModel, SetProductStatusModel, SubscribeProductModel


class HouseholdService:
    @staticmethod
    async def create_household(session: AsyncSession, household_data: HouseholdInfo):

        new_household = HouseholdORM(domain_id=household_data.domain,
                                     description=household_data.description,
                                     status=household_data.status,
                                     account_code=household_data.accnt_code,
                                     locale_id=household_data.locale_id,
                                     max_devices=household_data.max_devices,
                                     max_users=household_data.max_users,
                                     max_profiles=household_data.max_profiles,
                                     no_personalization=household_data.no_pers,
                                     )
        session.add(new_household)
        await session.commit()

        return new_household

    @staticmethod
    async def create_user(session: AsyncSession, user_data: UserInfo, household_id: int):

        new_user = UserORM(name=user_data.username,
                           password=hash_password_sha256(user_data.password),
                           first_name=user_data.first_name,
                           last_name=user_data.last_name,
                           status=user_data.status,
                           address=user_data.address,
                           phone=user_data.phone,
                           household_id=household_id
                           )
        session.add(new_user)
        await session.commit()

        return new_user

    @staticmethod
    async def create_profile(session: AsyncSession, profile_data: CreateProfileModel):
        new_profile = ClientProfileORM(household_id=profile_data.household_id,
                                       description=profile_data.description,
                                       age=profile_data.age,
                                       pin=profile_data.pin,
                                       purchase_pin=profile_data.purchase_pin,
                                       custom_data=profile_data.custom_data,
                                       type_id=profile_data.type,
                                       name=profile_data.name,
                                       image_urls=profile_data.images)
        session.add(new_profile)
        await session.commit()

        return new_profile

    @staticmethod
    async def set_user_profiles(session: AsyncSession, data: SetUserProfiles):
        for profile_id in data.profile_ids:
            new_user_profile = UserProfilesORM(user_id=data.user_id,
                                               profile_id=profile_id, )
            session.add(new_user_profile)
            await session.commit()
        return



    @staticmethod
    async def get_household(session):
        result = await session.execute(
            select(HouseholdORM)
            .options(joinedload(HouseholdORM.bundles))
        )

        result = result.scalars().unique().all()

        return result

    @staticmethod
    async def get_user(session):
        result = await session.execute(
            select(UserORM)
        )

        result = result.scalars().unique().all()

        return result

    @staticmethod
    async def get_household_by_id(session: AsyncSession, household_id: int):
        result = await session.execute(
            select(HouseholdORM)
            .where(HouseholdORM.id == household_id)
            .options(joinedload(HouseholdORM.bundles))
        )

        household = result.scalars().unique().one_or_none()
        return household

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int):
        result = await session.execute(
            select(UserORM)
            .where(UserORM.id == user_id)
        )
        user = result.scalar_one_or_none()
        return user

    @staticmethod
    async def get_household_products(session: AsyncSession):
        result = await session.execute(
            select(HouseholdToProductORM)
        )

        result = result.scalars().unique().all()


        return result

    @staticmethod
    async def get_subscriptions(session: AsyncSession, username: str):
        stmt = select(UserORM).where(
            UserORM.name == username,
        )

        user = await session.execute(stmt)
        user = user.scalar_one_or_none()

        household_id = int(user.household_id)
        stmt = select(HouseholdToProductORM).where(
            HouseholdToProductORM.household_id == household_id,
        )
        products = await session.execute(stmt)
        products = products.scalars().unique().all()

        return products

    @staticmethod
    async def get_user_profiles(session):
        result = await session.execute(
            select(UserProfilesORM)
        )

        result = result.scalars().unique().all()

        return result

        # response_data = {"response": 0}
        # if response_data == {"response": 0}:
        #     product = await session.execute(select(HouseholdORM))
        #     return product.scalars().all()
        # else:
        #     return

    # @staticmethod
    # async def update_household_info(session: AsyncSession,
    #                                 household_data: Union[UpdateHouseholdInfoModel, UpdateHouseholdModel]):
    #     response_data = {"response": 0}
    #     if response_data == {"response": 0}:
    #         household = await session.get(HouseholdORM, household_data.acc_code)
    #         if household:
    #             for key, value in household_data.dict(exclude_unset=True).items():
    #                 setattr(household, key, value)
    #             await session.commit()
    #             return household
    #     else:
    #         return None

    @staticmethod
    async def subscribe_product(session: AsyncSession, subscribe_data: SubscribeProductModel):

        new_subscribe = HouseholdToProductORM(**subscribe_data.dict(exclude_unset=True))
        session.add(new_subscribe)
        await session.commit()

        return new_subscribe

    #
    # @staticmethod
    # async def unsubscribe_product(session: AsyncSession, unsubscribe_data: UnsubscribeProductModel):
    #
    #     stmt = select(HouseholdToProductORM).where(
    #         HouseholdToProductORM.acc_code == unsubscribe_data.acc_code,
    #         HouseholdToProductORM.product_id == unsubscribe_data.product_id
    #     )
    #
    #     subscribe = await session.execute(stmt).scalars().first()
    #     if subscribe:
    #         setattr(subscribe, "is_enabled", False)
    #         await session.commit()
    #         return subscribe

    @staticmethod
    async def set_product_status(session: AsyncSession, set_data: SetProductStatusModel):

        stmt = select(HouseholdToProductORM).where(
            HouseholdToProductORM.household_id == set_data.household_id,
            HouseholdToProductORM.product_id == set_data.product_id
        )

        subscribe = await session.execute(stmt)
        subscribe = subscribe.scalar_one_or_none()
        if subscribe:
            subscribe.is_enabled = set_data.is_enabled
            await session.commit()
            return subscribe


household_service = HouseholdService()


def get_household_service() -> HouseholdService:
    return household_service
