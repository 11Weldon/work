from typing import Optional, Dict, List

from pydantic import Field

from src.models.utils import TunedModel


class ChannelModel(TunedModel):
    channel_id: Optional[int] = None
    service_id: str
    name: str
    type: str
    status: str
    format: int = 0
    mProv_id: int = 0
    cProv_id: int = 0
    langs: int = 0
    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    description: Optional[Dict[str, List[Dict[str, str]]]] = Field(default_factory=dict)
    custom: Optional[Dict[str, str]] = Field(default_factory=dict)
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    channel_urls: Optional[Dict[str, str]] = Field(default_factory=dict)

    class Config:
        orm_mode = True


class ListChannelModel(TunedModel):
    result: list[ChannelModel] = []


class CreateChannel(TunedModel):
    name: str
    type: str

