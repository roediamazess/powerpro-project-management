from typing import Optional
from pydantic import BaseModel, ConfigDict

class LookupBase(BaseModel):
    id: str
    name: str

class Lookup(LookupBase):
    model_config = ConfigDict(from_attributes=True)
