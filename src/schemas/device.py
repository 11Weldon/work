from typing import Optional, Dict

from pydantic import BaseModel, Field

from src.schemas.tuned_model import TunedModel


class DeviceSchema(TunedModel):
    external_id: str
    descr: str
    name: Optional[Dict[str, str]] = Field(default_factory=dict)

