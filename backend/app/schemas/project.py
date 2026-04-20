import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# --- PIC Schemas ---
class ProjectPICBase(BaseModel):
    user_id: uuid.UUID
    pic_role: Optional[str] = "MEMBER"

class ProjectPIC(ProjectPICBase):
    username: str
    fullname: str
    model_config = ConfigDict(from_attributes=True)

# --- Project Schemas ---
class ProjectBase(BaseModel):
    name: str
    partner_id: uuid.UUID
    cnc_id: Optional[str] = None
    type_id: Optional[str] = None
    status_id: Optional[str] = "PLANNING"
    arrangement_id: Optional[str] = None
    assignment_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    point_req: Optional[float] = 0.0

class ProjectCreate(ProjectBase):
    pic_ids: List[uuid.UUID] = []

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    status_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    pic_ids: Optional[List[uuid.UUID]] = None

class ProjectPartner(BaseModel):
    partner_id: uuid.UUID
    name: str
    model_config = ConfigDict(from_attributes=True)

class Project(ProjectBase):
    project_id: uuid.UUID
    total_days: Optional[int] = 0
    point_ach: Optional[float] = 0.0
    point_percent: Optional[float] = 0.0
    created_at: datetime
    updated_at: datetime
    partner: ProjectPartner
    pics: List[ProjectPIC] = []
    
    model_config = ConfigDict(from_attributes=True)
