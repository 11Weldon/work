from typing import Optional, Dict, List

from pydantic import Field

from backend.src.schemas.not_null import Omissible
from backend.src.schemas.tuned_model import TunedModel


class GroupProductSchema(TunedModel):
    external_id: Omissible[str]
    type: Omissible[str]
    status: Omissible[str]
    name: Omissible[str]
    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    descr: Optional[Dict[str, str]] = Field(default_factory=dict)
    custom: Optional[Dict[str, str]] = Field(default_factory=dict)
    prices: Optional[Dict[str, str]] = Field(default_factory=dict)
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class FeatureProductSchema(TunedModel):
    external_id: Omissible[str]
    status: Omissible[str]
    name: Omissible[str]
    quota: Omissible[int]
    valid_period: Omissible[int]
    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    descr: Optional[Dict[str, str]] = Field(default_factory=dict)
    custom: Optional[Dict[str, str]] = Field(default_factory=dict)
    prices: Optional[Dict[str, str]] = Field(default_factory=dict)
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class ProductSchema(TunedModel):
    title: Optional[Dict[str, str]] = Field(default_factory=dict)


