from typing import Optional, Dict, List

from pydantic import BaseModel, Field

from src.schemas.tuned_model import TunedModel


class UserSchema(TunedModel):
    username: str
    password: str
    first_name: str
    last_name: str
    status: str
    address: str
    phone: str
    hash_init: str


class HouseholdSchema(TunedModel):
    domain: int
    description: str
    status: str
    accnt_code: str
    locale_id: int
    max_devices: int
    max_users: int
    max_profiles: int
    no_pers: bool

    custom: Optional[Dict[str, Optional[object]]] = Field(default_factory=dict)

    class Config:
        orm_mode = True


class ProfileSchema(TunedModel):
    name: str
    type: str
    descr: str
    age: int
    pin: int
    purchasePin: int
    custom: Optional[Dict[str, str]] = Field(default_factory=dict)
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class HouseholdProducts(TunedModel):
    household_id: int
    product_ids: List[int]
