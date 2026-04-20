import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

# --- Contact Schemas ---
class PartnerContactBase(BaseModel):
    name: str
    position: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_primary: bool = False

class PartnerContactCreate(PartnerContactBase):
    pass

class PartnerContact(PartnerContactBase):
    contact_id: uuid.UUID
    partner_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# --- Partner Schemas ---
class PartnerBase(BaseModel):
    name: str
    partner_cnc: Optional[str] = None
    type_id: Optional[str] = None
    status_id: Optional[str] = None
    group_id: Optional[str] = None
    area_id: Optional[str] = None
    sub_area_id: Optional[str] = None
    version_id: Optional[str] = None
    imp_type_id: Optional[str] = None
    
    stars: Optional[int] = None
    rooms: Optional[int] = None
    outlets: Optional[int] = None
    address: Optional[str] = None
    system_live_at: Optional[datetime] = None
    last_visit_at: Optional[datetime] = None
    last_visit_type: Optional[str] = None
    last_project: Optional[datetime] = None
    last_project_type: Optional[str] = None

class PartnerCreate(PartnerBase):
    contacts: Optional[List[PartnerContactCreate]] = []

class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    partner_cnc: Optional[str] = None
    type_id: Optional[str] = None
    status_id: Optional[str] = None
    group_id: Optional[str] = None
    area_id: Optional[str] = None
    sub_area_id: Optional[str] = None
    version_id: Optional[str] = None
    imp_type_id: Optional[str] = None
    stars: Optional[int] = None
    rooms: Optional[int] = None
    outlets: Optional[int] = None
    address: Optional[str] = None
    system_live_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    last_visit_at: Optional[datetime] = None
    last_visit_type: Optional[str] = None
    last_project: Optional[datetime] = None
    last_project_type: Optional[str] = None
    contacts: Optional[List[PartnerContactBase]] = None

class Partner(PartnerBase):
    partner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    contacts: List[PartnerContact] = []
    
    model_config = ConfigDict(from_attributes=True)
