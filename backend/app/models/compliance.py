import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Text, Boolean, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base, PowerProBase

class ComplianceForm(Base, PowerProBase):
    __tablename__ = "compliance_forms"
    
    form_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    form_type: Mapped[Optional[str]] = mapped_column(String(10))
    item_count: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    listindex: Mapped[int] = mapped_column(default=0)
    
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    # Relationships
    items: Mapped[List["ComplianceItem"]] = relationship(secondary="compliance_form_items")
    entries: Mapped[List["ComplianceEntry"]] = relationship(back_populates="form")

class ComplianceItem(Base, PowerProBase):
    __tablename__ = "compliance_items"
    
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_code: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50))
    modbus_addr: Mapped[Optional[str]] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(default=True)
    listindex: Mapped[int] = mapped_column(default=0)
    
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))

class ComplianceFormItem(Base):
    __tablename__ = "compliance_form_items"
    form_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("compliance_forms.form_id"), primary_key=True)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("compliance_items.item_id"), primary_key=True)
    weight: Mapped[int] = mapped_column(Integer, default=1)
    listindex: Mapped[int] = mapped_column(default=0)

class ComplianceEntry(Base, PowerProBase):
    __tablename__ = "compliance_entries"
    
    entry_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("compliance_forms.form_id"))
    partner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("partners.partner_id"))
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.project_id"))
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    
    audit_phase: Mapped[Optional[str]] = mapped_column(String(20)) # REGULAR, BEFORE, AFTER
    baseline_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("compliance_entries.entry_id"))
    status: Mapped[Optional[str]] = mapped_column(String(20)) # DRAFT, SUBMITTED, VERIFIED
    
    location: Mapped[Optional[str]] = mapped_column(String(100))
    score_metric: Mapped[Optional[float]] = mapped_column(DECIMAL(10,2))
    score_max: Mapped[Optional[float]] = mapped_column(DECIMAL(10,2))
    compliance_percent: Mapped[Optional[float]] = mapped_column(DECIMAL(5,2))
    actual_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    # Relationships
    form: Mapped[ComplianceForm] = relationship(back_populates="entries")
    project: Mapped[Optional["Project"]] = relationship(back_populates="compliance_entries")
    scores: Mapped[List["ComplianceEntryScore"]] = relationship(back_populates="entry", cascade="all, delete-orphan")

class ComplianceEntryScore(Base):
    __tablename__ = "compliance_entry_scores"
    
    entry_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("compliance_entries.entry_id"), primary_key=True)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("compliance_items.item_id"), primary_key=True)
    
    score: Mapped[Optional[int]] = mapped_column(Integer)
    remark: Mapped[Optional[str]] = mapped_column(Text)
    photo_url: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    entry: Mapped[ComplianceEntry] = relationship(back_populates="scores")
    item: Mapped[ComplianceItem] = relationship()
