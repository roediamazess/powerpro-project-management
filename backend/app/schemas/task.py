import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# --- Task Schemas ---
class TaskBase(BaseModel):
    description: str
    task_no: Optional[str] = None
    project_id: Optional[uuid.UUID] = None
    partner_id: Optional[uuid.UUID] = None
    priority_id: Optional[str] = None
    status_id: Optional[str] = "OPEN"
    dept_id: Optional[str] = None
    assignee_id: Optional[uuid.UUID] = None
    action_solution: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    description: Optional[str] = None
    status_id: Optional[str] = None
    priority_id: Optional[str] = None
    assignee_id: Optional[uuid.UUID] = None
    action_solution: Optional[str] = None

class TaskPartner(BaseModel):
    partner_id: uuid.UUID
    name: str
    model_config = ConfigDict(from_attributes=True)

class TaskProject(BaseModel):
    project_id: uuid.UUID
    name: str
    model_config = ConfigDict(from_attributes=True)

class Task(TaskBase):
    task_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    project: Optional[TaskProject] = None
    model_config = ConfigDict(from_attributes=True)

# --- Timebox Schemas ---
class TimeboxBase(BaseModel):
    activity_name: str
    start_time: datetime
    end_time: datetime
    task_id: Optional[uuid.UUID] = None
    project_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    color_code: Optional[str] = "cyan"
    is_completed: bool = False

class TimeboxCreate(TimeboxBase):
    pass

class TimeboxUpdate(BaseModel):
    activity_name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_completed: Optional[bool] = None

class Timebox(TimeboxBase):
    timebox_id: uuid.UUID
    user_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
