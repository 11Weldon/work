from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    status: str
    address: str
    phone: str
    hash_init: str


class HouseholdSchema(BaseModel):
    household_id: int
    domain: int
    description: str
    status: str
    accnt_code: str
    locale_id: int
    max_devices: int
    max_users: int
    max_profiles: int
    no_pers: bool
    custom: Optional[Dict[str, Optional[str]]] = Field(default_factory=dict)

    class Config:
        orm_mode = True


class CreateHouseholdExtRequest(BaseModel):
    user: UserSchema
    household: HouseholdSchema
    custom: Optional[Dict[str, Optional[object]]] = Field(default_factory=dict)
