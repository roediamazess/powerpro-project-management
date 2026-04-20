from pydantic import BaseModel
from typing import Optional

class LookupBase(BaseModel):
    name: str
    listindex: int = 0
    is_active: bool = True

class LookupCreate(LookupBase):
    id: str

class LookupUpdate(BaseModel):
    name: Optional[str] = None
    listindex: Optional[int] = None
    is_active: Optional[bool] = None

class Lookup(LookupBase):
    id: str
    class Config:
        from_attributes = True

# Specialized for Sub-Areas
class SubAreaBase(LookupBase):
    area_id: str

class SubAreaCreate(SubAreaBase):
    id: str

class SubAreaUpdate(BaseModel):
    name: Optional[str] = None
    area_id: Optional[str] = None
    listindex: Optional[int] = None
    is_active: Optional[bool] = None

class SubArea(SubAreaBase):
    id: str
    class Config:
        from_attributes = True
