from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.queries import product
from src.schemas.product import GroupProductSchema, FeatureProductSchema

product_router = APIRouter()


@product_router.post("/op_facade/prodMgmt/CreateGroupProduct")
async def create_group_product(group_product_data: GroupProductSchema,
                               session: AsyncSession = Depends(get_db)
                               ):
    try:
        new_group_product = await product.add_group_product(session, group_product_data)
        return new_group_product
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@product_router.post("/op_facade/prodMgmt/CreateFeatureProduct")
async def create_feature_product(feature_product_data: FeatureProductSchema,
                                 session: AsyncSession = Depends(get_db)
                                 ):
    try:
        new_feature_product = await product.add_feature_product(session, feature_product_data)
        return new_feature_product
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
