from typing import Optional, Dict

from pydantic import BaseModel, Field


class DeviceSchema(BaseModel):
    external_id: str
    descr: str
    name: Optional[Dict[str, str]] = Field(default_factory=dict)

