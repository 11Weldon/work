from typing import Optional, Dict, List

from pydantic import Field, BaseModel


class ChannelSchema(BaseModel):
    service_id: int
    name: str
    type: str
    status: str
    format: int
    mProv_id: int
    cProv_id: int
    langs: int

    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    descr: Optional[Dict[str, List[Dict[str, str]]]] = Field(default_factory=dict)
    custom: Optional[Dict[str, str]] = Field(default_factory=dict)
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)

    class Config:
        orm_mode = True


class ChannelLiveUrlsSchema(BaseModel):
    channel_id: int
    channel_urls: Optional[List[Dict[str, str]]] = Field(default_factory=list)

    class Config:
        orm_mode = True


class SetGroupProductServicesRequest(BaseModel):
    group_product_id: int
    service_ids: List[int]


class ProductSchema(BaseModel):
    title: Optional[Dict[str, str]] = Field(default_factory=dict)

    class Config:
        orm_mode = True
        from_attributes = True


class ServicesList(BaseModel):
    target_type: str
    target_id: int
    name: str
    type: str
    seqNum: int
    inheritable: bool
    locked: bool

    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    descr: Optional[Dict[str, str]] = Field(default_factory=dict)
    entry_ids: Optional[List[str]] = Field(default_factory=list)
    entry_lsns: Optional[List[int]] = Field(default_factory=list)
