from typing import Optional, Dict

from pydantic import Field

from src.models.tuned_model import TunedModel


class DeviceSchema(TunedModel):
    external_id: str
    description: str
    name: Optional[Dict[str, str]] = Field(default_factory=dict)

