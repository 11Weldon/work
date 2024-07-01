from typing import List

from pydantic import BaseModel


class ClientSchema(BaseModel):
    balance: int
    id: int
    name: str


class BundleSchema(BaseModel):
    id: int
    title: str


class ChannelSchema(BaseModel):
    id: int
    title: str


class BundleWithChannelsSchema(BaseModel):
    id: int
    title: str
    channels: List[ChannelSchema]


class ClientWithBundlesSchema(BaseModel):
    id: int
    name: str
    balance: int
    bundles: List[BundleSchema]
