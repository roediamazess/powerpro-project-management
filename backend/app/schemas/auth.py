import uuid
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

class RoleBase(BaseModel):
    role_id: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    listindex: int = 0

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    listindex: Optional[int] = None

class Role(RoleBase):
    model_config = ConfigDict(from_attributes=True)

# -----------------------------------------------------------------------------

class TierBase(BaseModel):
    tier_id: str
    name: str
    is_active: bool = True
    listindex: int = 0

class TierCreate(TierBase):
    pass

class Tier(TierBase):
    model_config = ConfigDict(from_attributes=True)

# -----------------------------------------------------------------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr
    fullname: str
    is_active: bool = True
    role_id: Optional[str] = None
    tier_id: Optional[str] = None
    start_work: Optional[date] = None
    birthday: Optional[date] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[str] = None
    tier_id: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserInDB(User):
    password_hash: str
