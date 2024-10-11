from typing import Optional

from operatorfacade.src.zappware.operator_facade.models.household import HouseholdInfo
from operatorfacade.src.zappware.operator_facade.models.user import UserInfo
from pydantic import Field, Json

from src.enums.unlisted import HouseholdStatus
from src.models.primitive import OFdatetime, OFIntDtMap, OFStrDtMap, OFStrIntMap, OFIntIntMap
from src.models.utils import TunedModel


class HouseholdCustomData(TunedModel):
    advertising: bool
    recording_tcs: OFIntDtMap | None = None
    denied_recording_tcs: list[int] | None = None
    adult_content: bool
    tcs_agreed: bool
    track_viewing_behaviour: bool
    onboarding: OFStrDtMap | None = None
    preview_mode_allowed: bool | None = None
    billing_code: str
    bandwidths: OFStrIntMap
    multiscreen: bool
    EST_view: bool
    max_devices: OFIntIntMap
    max_concurrent_streams: OFStrIntMap
    max_paired_devices: int | None = None
    max_paired_devices_per_asset: int | None = None
    master_pin_code: str | None = None
    consents: OFStrDtMap | None = None
    denied_consents: OFStrDtMap | None = None


class HouseholdEntity(TunedModel):
    # 19.52
    domain_id: int
    contact: int | None = None
    description: str
    created: OFdatetime | None = None
    status: HouseholdStatus
    account_code: str
    locale_id: int
    max_devices: int
    max_users: int
    max_profiles: int
    no_personalization: bool | None = None
    time_stamp: OFdatetime | None = None


class UserEntity(TunedModel):
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    user_status: str | None = None
    address: str | None = None
    phone: str | None = None
    hashed_password: Optional[bool] = False
    hash_init: Optional[str] | None = None


class CreateHouseholdModel(TunedModel):
    household: HouseholdInfo | None = None
    user: UserInfo | None = None
    hashed_password: bool | None = False
    custom_data: Json[HouseholdCustomData] | None = None

class UpdateHouseholdInfoModel(TunedModel):
    acc_code: str
    first_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    username: Optional[str]
    hashed_pwd: Optional[bool]
    password: Optional[str]
    hash_init: Optional[str]


class UpdateHouseholdModel(TunedModel):
    acc_code: str
    domain_id: Optional[int]
    is_enabled: Optional[bool]
    no_pers: Optional[bool]
    master_PIN: Optional[str] = Field(..., max_length=4)


class SubscribeProductModel(TunedModel):
    acc_code: str
    product_id: str
    is_enabled: bool


class UnsubscribeProductModel(TunedModel):
    acc_code: str
    product_id: str


class SetProductStatusModel(TunedModel):
    acc_code: str
    product_id: str
    is_enabled: bool
