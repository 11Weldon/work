from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product import GroupProduct, FeatureProduct


async def add_group_product(session: AsyncSession, group_product_data):
    try:
        new_group_product = GroupProduct(**group_product_data.dict())
        session.add(new_group_product)
        await session.commit()
        return {"response": new_group_product.group_product_id}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


async def add_feature_product(session: AsyncSession, feature_product_data):
    try:
        new_feature_product = FeatureProduct(**feature_product_data.dict())
        session.add(new_feature_product)
        await session.commit()
        return {"response": new_feature_product.feature_product_id}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(ex)}")
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


