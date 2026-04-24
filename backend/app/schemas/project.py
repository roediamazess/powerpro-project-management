import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, AliasPath

# --- PIC Schemas ---
class ProjectPICBase(BaseModel):
    user_id: uuid.UUID
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
    s1_count_email_sent: Optional[str] = None
    s2_email_sent: Optional[str] = None
    s3_email_sent: Optional[str] = None
    
    pyear: Optional[int] = None
    pquarter: Optional[str] = None
    pmonth: Optional[str] = None
    pweekno: Optional[str] = None
    pweekofmonth: Optional[str] = None

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
    
    # Extended Fields
    handover_or: Optional[datetime] = None
    handover_days: Optional[int] = None
    pic_kpi_2: Optional[float] = None
    check_or: Optional[datetime] = None
    check_days: Optional[int] = None
    officer_kpi2: Optional[float] = None
    validation_date: Optional[datetime] = None
    validation_days: Optional[int] = None
    okr_kpi2: Optional[float] = None
    
    s1_estimation: Optional[datetime] = None
    s1_over_days: Optional[int] = None
    s1_count_email_sent: Optional[str] = None
    s2_email_sent: Optional[str] = None
    s3_email_sent: Optional[str] = None
    
    pyear: Optional[int] = None
    pquarter: Optional[str] = None
    pmonth: Optional[str] = None
    pweekno: Optional[str] = None
    pweekofmonth: Optional[str] = None

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
