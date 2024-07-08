from typing import Optional, Dict, List

from pydantic import Field, BaseModel

from src.schemas.tuned_model import TunedModel


class GroupProductSchema(TunedModel):
    external_id: str
    type: str
    status: str
    name: str
    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    descr: Optional[Dict[str, str]] = Field(default_factory=dict)
    custom: Optional[Dict[str, str]] = Field(default_factory=dict)
    prices: Optional[Dict[str, str]] = Field(default_factory=dict)
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class FeatureProductSchema(TunedModel):
    external_id: str
    status: str
    name: str
    quota: int
    valid_period: int
    title: Optional[Dict[str, str]] = Field(default_factory=dict)
    descr: Optional[Dict[str, str]] = Field(default_factory=dict)
    custom: Optional[Dict[str, str]] = Field(default_factory=dict)
    prices: Optional[Dict[str, str]] = Field(default_factory=dict)
    image: Optional[List[Dict[str, str]]] = Field(default_factory=list)


