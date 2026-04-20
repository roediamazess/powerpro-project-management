import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

# --- Compliance Item ---
class ComplianceItemBase(BaseModel):
    item_code: Optional[str] = None
    name: str
    category: Optional[str] = None
    modbus_addr: Optional[str] = None
    listindex: int = 0

class ComplianceItem(ComplianceItemBase):
    item_id: uuid.UUID
    weight: int = 1
    model_config = ConfigDict(from_attributes=True)

# --- Compliance Form ---
class ComplianceFormBase(BaseModel):
    form_code: str
    name: str
    form_type: str = "REGULAR"
    is_active: bool = True

class ComplianceForm(ComplianceFormBase):
    form_id: uuid.UUID
    items: List[ComplianceItem] = []
    model_config = ConfigDict(from_attributes=True)

# --- Compliance Scores ---
class EntryScoreBase(BaseModel):
    item_id: uuid.UUID
    score: int = Field(..., ge=0, le=5)
    remark: Optional[str] = None
    photo_url: Optional[str] = None

class EntryScoreRead(EntryScoreBase):
    item: ComplianceItem
    model_config = ConfigDict(from_attributes=True)

# --- Compliance Entries ---
class ComplianceEntryBase(BaseModel):
    form_id: uuid.UUID
    partner_id: uuid.UUID
    project_id: Optional[uuid.UUID] = None
    baseline_id: Optional[uuid.UUID] = None
    audit_phase: str = "REGULAR"
    location: Optional[str] = None
    status: str = "SUBMITTED"
    actual_date: Optional[datetime] = None

class ComplianceEntryCreate(ComplianceEntryBase):
    scores: List[EntryScoreBase]

class ComplianceEntryRead(ComplianceEntryBase):
    entry_id: uuid.UUID
    agent_id: uuid.UUID
    score_metric: float
    score_max: float
    compliance_percent: float
    improvement_percent: Optional[float] = 0.0
    created_at: datetime
    form: ComplianceForm
    scores: List[EntryScoreRead] = []
    
    model_config = ConfigDict(from_attributes=True)
