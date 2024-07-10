from typing import Optional, Dict, List

from pydantic import Field

from backend.src.schemas.not_null import Omissible
from backend.src.schemas.tuned_model import TunedModel


class UserSchema(TunedModel):
    username: Omissible[str]
    password: Omissible[str]
    first_name: Omissible[str]
    last_name: Omissible[str]
    status: Omissible[str]
    address: Omissible[str]
    phone: Omissible[str]
    hash_init: Omissible[str]


class HouseholdSchema(TunedModel):
    domain: Omissible[int]
    description: Omissible[str]
    status: Omissible[str]
    accnt_code: Omissible[str]
    locale_id: Omissible[int]
    max_devices: Omissible[int]
    max_users: Omissible[int]
    max_profiles: Omissible[int]
    no_pers: Omissible[bool]

    custom: Optional[Dict[str, Optional[object]]] = Field(default_factory=dict)

    class Config:
        orm_mode = True


class ProfileSchema(TunedModel):
    name: Omissible[str]
    type: Omissible[str]
    descr: Omissible[str]
    age: Omissible[int]
    pin: Omissible[int]
    purchasePin: Omissible[int]
    custom: Optional[Dict[str, str]] = Field(default_factory=dict)
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class HouseholdProducts(TunedModel):
    household_id: Omissible[int]
    product_ids: Omissible[List[int]]
