import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, AliasPath

# --- PIC Schemas ---
class ProjectPICBase(BaseModel):
    user_id: uuid.UUID
    pic_role: Optional[str] = "MEMBER"
    arrangement_id: Optional[str] = "SELF"
    assignment_id: Optional[str] = "SELF"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_days: Optional[int] = 1
    status: Optional[str] = "OPEN"

class ProjectPIC(ProjectPICBase):
    username: str = Field(validation_alias=AliasPath("user", "username"))
    fullname: str = Field(validation_alias=AliasPath("user", "fullname"))
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
    information_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    point_req: Optional[float] = 0.0
    status: Optional[str] = "OPEN"
    
    # Extended Fields
    handover_or: Optional[datetime] = None
    handover_days: Optional[int] = 0
    pic_kpi_2: Optional[float] = 0.0
    
    check_or: Optional[datetime] = None
    check_days: Optional[int] = 0
    officer_kpi2: Optional[float] = 0.0
    
    validation_date: Optional[datetime] = None
    validation_days: Optional[int] = 0
    okr_kpi2: Optional[float] = 0.0
    
    s1_estimation: Optional[datetime] = None
    s1_over_days: Optional[int] = 0
    s1_count_email_sent: Optional[int] = 0
    s2_email_sent: Optional[int] = 0
    s3_email_sent: Optional[int] = 0
    
    pyear: Optional[int] = None
    pquarter: Optional[int] = None
    pmonth: Optional[int] = None
    pweekno: Optional[int] = None
    pweekofmonth: Optional[int] = None

class ProjectCreate(ProjectBase):
    pic_assignments: List[ProjectPICBase] = []

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    cnc_id: Optional[str] = None
    partner_id: Optional[uuid.UUID] = None
    type_id: Optional[str] = None
    status: Optional[str] = None
    status_id: Optional[str] = None
    information_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    point_req: Optional[float] = None
    pic_assignments: Optional[List[ProjectPICBase]] = None

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
    pic_assignments: List[ProjectPIC] = []
    
    model_config = ConfigDict(from_attributes=True)
