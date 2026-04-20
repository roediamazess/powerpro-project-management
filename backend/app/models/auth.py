import uuid
from typing import Optional, List
from datetime import date
from sqlalchemy import String, ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base, PowerProBase

class Role(Base, PowerProBase):
    __tablename__ = "roles"
    
    role_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    listindex: Mapped[int] = mapped_column(default=0)
    
    users: Mapped[List["User"]] = relationship(back_populates="role")

class Tier(Base, PowerProBase):
    __tablename__ = "tiers"
    
    tier_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    listindex: Mapped[int] = mapped_column(default=0)
    
    users: Mapped[List["User"]] = relationship(back_populates="tier")

class User(Base, PowerProBase):
    __tablename__ = "users"
    
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    
    role_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("roles.role_id"))
    tier_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("tiers.tier_id"))
    
    start_work: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    role: Mapped[Optional[Role]] = relationship(back_populates="users")
    tier: Mapped[Optional[Tier]] = relationship(back_populates="users")
