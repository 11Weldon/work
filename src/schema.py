from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class ClientSchema(BaseModel):
    balance: int
    id: int
    name: str


class ProductSchema(BaseModel):
    id: int
    title: str


class ServiceIdsSchema(BaseModel):
    Service_ids: List[int]


class ChannelSchema(BaseModel):
    id: int
    title: str
    synopsis_short: Optional[Dict[str, str]] = Field(default_factory=dict)
    synopsis_long: Optional[Dict[str, str]] = Field(default_factory=dict)
    keywords: Optional[Dict[str, List[Dict[str, str]]]] = Field(default_factory=dict)
    audio: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class ProductWithChannelsSchema(BaseModel):
    id: int
    title: str
    channels: List[ChannelSchema]


class ClientWithProductsSchema(BaseModel):
    id: int
    name: str
    balance: int
    products: List[ProductSchema]


class DomainSchema(BaseModel):
    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    descr: Optional[Dict[str, str]] = Field(default_factory=dict)


class ChannelMappingSchema(BaseModel):
    channelId: int
    targetId: int
    type: str
    mapped: str
