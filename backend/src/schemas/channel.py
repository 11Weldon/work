from typing import Optional, Dict, List

from pydantic import Field

from backend.src.schemas.not_null import Omissible
from backend.src.schemas.tuned_model import TunedModel


class ChannelSchema(TunedModel):
    service_id: Omissible[int]
    name: Omissible[str]
    type: Omissible[str]
    status: Omissible[str]
    format: Omissible[int]
    mProv_id: Omissible[int]
    cProv_id: Omissible[int]
    langs: Omissible[int]

    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    descr: Optional[Dict[str, List[Dict[str, str]]]] = Field(default_factory=dict)
    custom: Optional[Dict[str, str]] = Field(default_factory=dict)
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)

    class Config:
        orm_mode = True


class ChannelLiveUrlsSchema(TunedModel):
    channel_id: Omissible[int]
    channel_urls: Optional[List[Dict[str, str]]] = Field(default_factory=list)

    class Config:
        orm_mode = True


class SetGroupProductServicesRequest(TunedModel):
    group_product_id: Omissible[int]
    service_ids: Omissible[List[int]]


class ProductSchema(TunedModel):
    title: Optional[Dict[str, str]] = Field(default_factory=dict)

    class Config:
        orm_mode = True
        from_attributes = True


class ServicesList(TunedModel):
    target_type: Omissible[str]
    target_id: Omissible[int]
    name: Omissible[str]
    type: Omissible[str]
    seqNum: Omissible[int]
    inheritable: Omissible[bool]
    locked: Omissible[bool]

    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    descr: Optional[Dict[str, str]] = Field(default_factory=dict)
    entry_ids: Optional[List[str]] = Field(default_factory=list)
    entry_lsns: Optional[List[int]] = Field(default_factory=list)
