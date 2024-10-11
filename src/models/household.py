from typing import Optional

from pydantic import Field, Json

from src.enums.unlisted import HouseholdStatus, UserStatus
from src.models.primitive import OFdatetime, OFIntDtMap, OFStrDtMap, OFStrIntMap, OFIntIntMap, OFStrStrMap
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
    domain_id: int | None = None
    contact: int | None = None
    description: str | None = None
    created: OFdatetime | None = None
    status: HouseholdStatus | None = None
    account_code: str | None = None
    locale_id: int | None = None
    custom_data: Json[HouseholdCustomData] | None = None
    max_devices: int | None = None
    max_users: int | None = None
    max_profiles: int | None = None
    no_personalization: bool | None = None
    time_stamp: OFdatetime | None = None


class UserEntity(TunedModel):
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    status: UserStatus | None = None
    address: str | None = None
    phone: str | None = None
    hashed_password: Optional[str] = False


class HouseholdInfo(TunedModel):
    # 19.50
    domain: int
    description: str
    status: int
    accnt_code: str
    locale_id: int
    max_devices: int
    max_users: int
    max_profiles: int
    no_pers: bool

    # @field_serializer("status")
    # def serialize_status(self, status: HouseholdStatus, _info: Any):
    #     if isinstance(status, int):
    #         status = HouseholdStatus(status)
    #     return status.name


class UserInfo(TunedModel):
    # 19.49
    username: str
    password: str
    first_name: str
    last_name: str
    status: int
    address: str
    phone: str
    hash_init: str | None = None

    # @field_serializer("status")
    # def serialize_status(self, status: UserStatus, _info: Any):
    #     if isinstance(status, int):
    #         status = UserStatus(status)
    #     return status.name


class CreateHouseholdModel(TunedModel):
    household: HouseholdInfo | None = None
    user: UserInfo | None = None
    hashed_password: bool | None = False
    custom_data: str | None = None


class SetUserProfiles(TunedModel):
    user_id: int
    profile_ids: list[int]
    default_profile_id: int


class ChPrefObject(TunedModel):
    audio_language: str | None = None
    subtitle_language: str | None = None
    blocked: bool | None = None


class ClientProfileCustomData(TunedModel):
    active_channel_list: str
    active_channel: str
    budget_limit: int
    language: str
    onboarding: OFStrDtMap | None = None
    view_blocked_channels: bool | None = None
    first_audio_language: str | None = None
    first_subtitle_language: str | None = None
    second_audio_language: str | None = None
    second_subtitle_language: str | None = None
    channel_preferences: dict[str, ChPrefObject] | None = None
    mask_content: bool | None = None
    protection: str | None = None
    hard_of_hearing: bool | None = None
    visually_impaired: bool | None = None
    channel_list_order: list[str] | None = None
    avatar: str | None = None
    logout_pin: str | None = None
    adult_content: bool | None = None
    track_viewing_behaviour: bool | None = None
    manage_channel_lists: bool | None = None
    single_channel_list: str | None = None
    access_search: bool | None = None
    manage_recordings: bool | None = None
    can_sort_apps: bool | None = None
    can_manage_apps: bool | None = None
    can_purchase: bool | None = None
    purchase_protection: str | None = None
    active_channel_lists: OFStrStrMap | None = None
    active_channels: OFStrStrMap | None = None
    consents: OFStrDtMap | None = None
    denied_consents: OFStrDtMap | None = None


class ProfileType(TunedModel):
    # 19.58
    id: int
    title: Json[OFStrStrMap]
    description: Json[OFStrStrMap]
    custom_data: str
    image_urls: OFStrStrMap
    time_stamp: OFdatetime


class CreateProfileModel(TunedModel):
    household_id: int
    name: str
    description: str
    type: int
    age: int
    pin: str
    purchase_pin: str
    custom_data: str | None = None
    images: OFStrStrMap | None = None
    mediaIds: list[int] | None = None
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
