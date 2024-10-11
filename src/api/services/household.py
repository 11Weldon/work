from typing import Union

from operatorfacade.src.zappware.operator_facade.models.household import HouseholdInfo
from operatorfacade.src.zappware.operator_facade.models.user import UserInfo
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.dal.schemas.household import HouseholdORM, UserORM
from src.models.household import UpdateHouseholdInfoModel, UpdateHouseholdModel, HouseholdEntity


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
    async def create_user(session: AsyncSession, user_data: UserInfo):

        new_user = UserORM(name=user_data.username,
                           password=user_data.password,
                           first_name=user_data.first_name,
                           last_name=user_data.last_name,
                           status=user_data.status,
                           address=user_data.address,
                           phone=user_data.phone,
                           )
        session.add(new_user)
        await session.commit()

        return new_user

    @staticmethod
    async def get_household(session):
        result = await session.execute(
            select(HouseholdORM)
            .options(joinedload(HouseholdORM.bundles))
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

    # @staticmethod
    # async def subscribe_product(session: AsyncSession, subscribe_data: SubscribeProductModel):
    #     response_data = {"response": 0}
    #     if response_data == {"response": 0}:
    #         new_subscribe = HouseholdToProductORM(
    #             **subscribe_data.dict(exclude_unset=True),
    #             household_to_product_id=f"{subscribe_data.acc_code} {subscribe_data.product_id}")
    #         session.add(new_subscribe)
    #         await session.commit()
    #
    #         return new_subscribe
    #     else:
    #         return
    #
    # @staticmethod
    # async def unsubscribe_product(session: AsyncSession, unsubscribe_data: UnsubscribeProductModel):
    #     response_data = {"response": 0}
    #     if response_data == {"response": 0}:
    #         subscribe = await session.get(HouseholdToProductORM, f"{unsubscribe_data.acc_code} {unsubscribe_data.product_id}")
    #         if subscribe:
    #             setattr(subscribe, "is_enabled", False)
    #             await session.commit()
    #             return subscribe
    #     else:
    #         return
    #
    # @staticmethod
    # async def set_product_status(session: AsyncSession, set_data: SetProductStatusModel):
    #     response_data = {"response": 0}
    #     if response_data == {"response": 0}:
    #         subscribe = await session.get(HouseholdToProductORM, f"{set_data.acc_code} {set_data.product_id}")
    #         if subscribe:
    #             setattr(subscribe, "is_enabled", set_data.is_enabled)
    #             await session.commit()
    #             return subscribe
    #     else:
    #         return


household_service = HouseholdService()


def get_household_service() -> HouseholdService:
    return household_service
