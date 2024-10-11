from pydantic import BaseModel, Json

from src.models.utils import TunedModel
from .primitive import OFdatetime, OFStrStrMap
from ..enums.unlisted import BundleDisplayType


class BundleCustomData(TunedModel):
    subtitle: OFStrStrMap | None = None
    display_type: BundleDisplayType | None = None


class BundleProduct(TunedModel):
    # 19.29
    id: int
    external_id: str
    name: str


class BundleModel(TunedModel):
    # 19.29
    external_id: str
    name: str
    title: Json[OFStrStrMap] | None = None
    description: Json[OFStrStrMap] | None = None
    is_add_on: bool | None = None
    custom_data: Json[BundleCustomData] | None = None
    # products: list[BundleProduct] | None = None
    image_urls: OFStrStrMap | None = None
    time_stamp: OFdatetime | None = None


# class BundleModel(TunedModel):
#     bundle_id: str
#     name: str
#     price: str
#     title: dict
#     description: dict
#     image_urls: dict


class UpsellBundle(TunedModel):
    # 19.118
    bundle_id: str
    valid_intv: int | None = None
    price: int | None = None
    currency_id: int | None = None
    coupon_description: str | None = None
    price_w_coupon: int | None = None
    upsell_in_progress: bool | None = None
    selfcare_url: str | None = None


class UpsellTarget(TunedModel):
    # 19.118
    target: str | None = None
    trigger: str | None = None
    bundles: list[UpsellBundle]


class UpsellBundleResult(TunedModel):
    # 19.118  described as UpsellBundle 1st case
    targets: list[UpsellTarget]
    transaction_id: str


class UpsellBundleRequest(TunedModel):
    locale_id: int | None = None
    user_id: int | None = None
    profile_id: int | None = None
    device_id: str | None = None
    household_id: int | None = None
    account_code: str | None = None
    trigger: str | None = None
    target: str | None = None


class GetUpsellInfoModel(TunedModel):
    acc_code: str
    trigger_type: str
    trigger_id: str


class ResUpsellInfoModel(TunedModel):
    transaction_id: str
    bundles: list[BundleModel]


class UpsellInfoModel(TunedModel):
    transaction_id: str
    acc_code: str
    trigger_type: str
    trigger_id: str


class AddBundleToUpsell(TunedModel):
    transaction_id: int
    bundle_id: int


class PurchaiseBundleModel(TunedModel):
    transaction_id: str
    bundle_id: str | None = None
    price: int | None = None
    currency_id: int | None = None
    coupon_code: str | None = None

