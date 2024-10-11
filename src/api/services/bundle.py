import json

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.services import redis_client
from src.dal.schemas.bundle import BundleORM, product_bundle_association, \
    bundle_household_association
from src.dal.schemas.product import ProductORM
from src.models.bundle import BundleModel, PurchaiseBundleModel, UpsellBundleRequest, UpsellTarget, \
    UpsellBundleResult, UpsellBundle
from src.models.product import AddProductToBundle


class BundleService:
    @staticmethod
    async def create_bundle(session: AsyncSession, bundle_data: BundleModel):
        new_bundle = BundleORM(**bundle_data.dict(exclude_unset=True))
        session.add(new_bundle)
        await session.commit()

        return new_bundle

    @staticmethod
    async def get_bundle(session: AsyncSession):

        # product = await session.execute(select(BundleORM))

        result = await session.execute(
            select(BundleORM)
            .options(joinedload(BundleORM.products))
        )

        result = result.scalars().unique().all()
        return result

    # @staticmethod
    # async def create_upsell_info(session: AsyncSession, upsell_info_data: UpsellInfoModel):
    #
    #     response_data = {"response": 0}
    #     if response_data == {"response": 0}:
    #         new_upsell = UpsellInfo(**upsell_info_data.dict(exclude_unset=True))
    #         session.add(new_upsell)
    #         await session.commit()
    #
    #         return new_upsell
    #     else:
    #         return

    # @staticmethod
    # async def add_bundle_to_upsell(session: AsyncSession, bundle_data: AddBundleToUpsell):
    #
    #     bundle = await session.get(BundleORM, bundle_data.bundle_id)
    #     upsell_info = await session.get(UpsellInfo, bundle_data.transaction_id)
    #
    #     if bundle and upsell_info:
    #         stmt = insert(bundle_upsell_association).values(bundle_id=bundle_data.bundle_id,
    #                                                         transaction_id=bundle_data.transaction_id)
    #         await session.execute(stmt)
    #         await session.commit()
    #         return {"status": "200", "message": f"{bundle_data.bundle_id=}, {bundle_data.transaction_id=}"}
    #     else:
    #         return {"status": "error", "message": "Bundle or UpsellInfo not found"}

    @staticmethod
    async def add_product_to_bundle(session: AsyncSession, add_data: AddProductToBundle):
        bundle = await session.get(BundleORM, add_data.bundle_id)
        product = await session.get(ProductORM, add_data.product_id)

        if bundle and product:
            stmt = insert(product_bundle_association).values(bundle_id=add_data.bundle_id,
                                                             product_id=add_data.product_id)
            await session.execute(stmt)
            await session.commit()
            return {"status": "200", "message": f" bundle_id={add_data.bundle_id}, product_id={add_data.product_id}"}
        else:
            return {"status": "error", "message": "Bundle or Product not found"}

    @staticmethod
    async def get_upsell_info(session: AsyncSession, upsell_info_data: UpsellBundleRequest):

        # response_data = {"response": 0}
        # if response_data == {"response": 0}:
        #     result = await session.execute(
        #         select(UpsellInfo)
        #         .options(joinedload(UpsellInfo.bundle_list))
        #         .where(UpsellInfo.acc_code == upsell_info_data.acc_code,
        #                UpsellInfo.trigger_type == upsell_info_data.trigger_type)
        #     )
        #
        #     upsell_info = result.scalars().unique().all()

        result = await session.execute(
            select(BundleORM)
            .options(joinedload(BundleORM.products))
        )

        bundles = result.scalars().unique().all()
        bundle_ids = [bundle.id for bundle in bundles]
        transaction_id = "string"

        key = transaction_id

        bundle_objects = [
            UpsellBundle(
                bundle_id=bundle.external_id,
            )
            for bundle in bundles
        ]

        upsell_bundle = UpsellBundleResult(
            targets=[
                UpsellTarget(
                    target="some_target",
                    trigger="some_trigger",
                    bundles=bundle_objects
                )
            ],
            transaction_id=transaction_id
        )

        await redis_client.set(key, json.dumps(upsell_bundle.model_dump()), ex=300)
        # Сохранение данных в Redis с временем жизни 5 минут (300 секунд)

        return {"transactionId": transaction_id,
                "bundles": upsell_bundle,
                "data": json.dumps(upsell_bundle.model_dump())}

    @staticmethod
    async def purchaise_bundle(session: AsyncSession, purchaise_data: PurchaiseBundleModel):
        # bundle = await session.get(BundleORM, purchaise_data.bundle_id)
        # household = await session.get(HouseholdORM, purchaise_data.acc_code)

        upsell_bundle = await redis_client.get(purchaise_data.transaction_id)
        upsell_bundle = json.loads(upsell_bundle.decode('utf-8'))

        bundle_ids = [bundle["bundle_id"] for bundle in upsell_bundle["targets"][0]["bundles"]]
        for bundle_id in bundle_ids:
            # func
            bundle = await session.execute(
                select(BundleORM).where(BundleORM.external_id == bundle_id)
            )
            bundle = bundle.scalars().first()
            #
            stmt = insert(bundle_household_association).values(bundle_id=int(bundle.id),
                                                               household_id=1)
            await session.execute(stmt)
        await session.commit()
        return {"status": "200", "message": f"{bundle_ids}"}
        return bundle_ids
        # if bundle and household:
        #     stmt = insert(bundle_household_association).values(bundle_id=purchaise_data.bundle_id,
        #                                                     household_id=purchaise_data.acc_code)
        #     await session.execute(stmt)
        #     await session.commit()
        #     return {"status": "200", "message": f"{purchaise_data.bundle_id=}, {purchaise_data.acc_code=}"}
        # else:
        #     return {"status": "error", "message": "Bundle or Household not found"}

        # response_data = {"response": 0}
        # if response_data == {"response": 0}:
        #
        #     upsell_info = await session.get(UpsellInfo, purchaise_data.transaction_id)
        #
        #     bundle = await session.get(BundleORM, purchaise_data.bundle_id)
        #     # IF MONEY
        #     new_product = ProductORM(product_id=f"b {purchaise_data.bundle_id}",
        #                              bundle_list=[bundle])
        #     if upsell_info and bundle and new_product:
        #
        #         # return {"ebat": "ee"}
        #         await HouseholdService.subscribe_product(session=session,
        #                                                  subscribe_data=SubscribeProductModel(
        #                                                      acc_code=upsell_info.acc_code,
        #                                                      product_id=new_product.product_id,
        #                                                      is_enabled=True))
        #         session.add(new_product)
        #         await session.commit()
        #         return {"deneg": "dostatochno"}
        #     else:
        #         return {"upsell_info": upsell_info,
        #                 "bundle": bundle,
        #                 "new_product": new_product}


bundle_service = BundleService()


def get_bundle_service() -> BundleService:
    return bundle_service
