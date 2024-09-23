from typing import Optional

from pydantic import Json

from src.enums.unlisted import ProductType, ProductStatus
from src.models.primitive import OFdatetime, OFStrStrMap
from src.models.utils import TunedModel


# class ProductModel(TunedModel):
#     product_id: str
#

class CreateProductModel(TunedModel):
    external_id: str
    type: Optional[ProductType] = None
    valid_start: Optional[OFdatetime] = None
    valid_end: Optional[OFdatetime] = None
    status: Optional[ProductStatus] = None
    # prices: list[ProductPrice]
    image_urls: Optional[OFStrStrMap] = None
    time_stamp: Optional[OFdatetime] = None
    name: Optional[str] = None
    title: Optional[Json[OFStrStrMap]] = None
    description: Optional[Json[OFStrStrMap]] = None
    feat_prod_id: int | None = None
    custom_data: str | None = None


class AddProductToBundle(TunedModel):
    bundle_id: int
    product_id: int


class ProductPrice(TunedModel):
    # 19.25
    id: int
    currency_id: int
    price: int
    valid_start: OFdatetime | None = None
    valid_end: OFdatetime | None = None


class ProductModel(TunedModel):
    # 19.28
    id: int
    external_id: str
    type: ProductType | None = None
    valid_start: OFdatetime | None = None
    valid_end: OFdatetime | None = None
    status: ProductStatus | None = None
    # prices: list[ProductPrice]
    image_urls: OFStrStrMap | None = None
    time_stamp: OFdatetime | None = None
    name: str | None = None
    title: Json[OFStrStrMap] | None = None
    description: Json[OFStrStrMap] | None = None
    feat_prod_id: int | None = None
    custom_data: str | None = None
