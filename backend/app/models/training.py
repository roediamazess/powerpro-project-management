import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base, PowerProBase

class ORTrainingSession(Base, PowerProBase):
    __tablename__ = "or_training_sessions"
    
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.project_id"), nullable=False)
    
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    trainer_name: Mapped[Optional[str]] = mapped_column(String(100))
    
    is_active: Mapped[bool] = mapped_column(default=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    project: Mapped["Project"] = relationship(back_populates="training_sessions")
    attendees: Mapped[List["ORTrainingAttendee"]] = relationship(back_populates="session", cascade="all, delete-orphan")

class ORTrainingAttendee(Base):
    __tablename__ = "or_training_attendees"
    
    attendee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("or_training_sessions.session_id"), nullable=False)
    
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)
    department: Mapped[Optional[str]] = mapped_column(String(100))
    position: Mapped[Optional[str]] = mapped_column(String(100))
    
    device_id: Mapped[Optional[str]] = mapped_column(String(255)) # IP + UA hash or similar
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    session: Mapped[ORTrainingSession] = relationship(back_populates="attendees")
