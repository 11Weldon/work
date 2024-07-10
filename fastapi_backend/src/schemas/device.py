from typing import Optional, Dict

from pydantic import Field

from src.schemas.not_null import Omissible
from src.schemas.tuned_model import TunedModel


class DeviceSchema(TunedModel):
    external_id: Omissible[str]
    descr: Omissible[str]
    name: Optional[Dict[str, str]] = Field(default_factory=dict)

