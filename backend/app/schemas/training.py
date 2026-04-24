import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ORTrainingAttendeeBase(BaseModel):
    fullname: str
    department: Optional[str] = None
    position: Optional[str] = None

class ORTrainingAttendeeCreate(ORTrainingAttendeeBase):
    session_id: uuid.UUID
    device_id: Optional[str] = None

class ORTrainingAttendee(ORTrainingAttendeeBase):
    attendee_id: uuid.UUID
    session_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ORTrainingSessionBase(BaseModel):
    project_id: uuid.UUID
    topic: str
    trainer_name: Optional[str] = None

class ORTrainingSessionCreate(ORTrainingSessionBase):
    pass

class ORTrainingSession(ORTrainingSessionBase):
    session_id: uuid.UUID
    is_active: bool
    expires_at: datetime
    created_at: datetime
    attendee_count: int = 0

    class Config:
        from_attributes = True

class ORTrainingSessionDetail(ORTrainingSession):
    attendees: List[ORTrainingAttendee] = []
