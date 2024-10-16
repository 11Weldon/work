from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dal.schemas.product import ProductORM


class ProductService:
    # @staticmethod
    # async def create_product(session: AsyncSession, product_data: CreateGroupProduct):
    #
    #     new_product = ProductORM(**product_data.dict(exclude_unset=True))
    #     session.add(new_product)
    #     await session.commit()
    #
    #     return new_product

    @staticmethod
    async def get_product(session: AsyncSession):

        response_data = {"response": 0}
        if response_data == {"response": 0}:
            product = await session.execute(select(ProductORM))
            return product.scalars().all()
        else:
            return


product_service = ProductService()


def get_product_service() -> ProductService:
    return product_service
