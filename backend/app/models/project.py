import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base, PowerProBase

# --- Lookup Tables ---
class ProjectType(Base):
    __tablename__ = "project_types"
    type_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

class ProjectStatus(Base):
    __tablename__ = "project_statuses"
    status_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

class ProjectArrangement(Base):
    __tablename__ = "project_arrangements"
    arrangement_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

class ProjectAssignment(Base):
    __tablename__ = "project_assignments"
    assignment_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

# --- Junction Table ---
class ProjectPIC(Base):
    __tablename__ = "project_pics"
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.project_id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    pic_role: Mapped[Optional[str]] = mapped_column(String(50))
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)

# --- Main Tables ---
class Project(Base, PowerProBase):
    __tablename__ = "projects"
    
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cnc_id: Mapped[Optional[str]] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    partner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("partners.partner_id"), nullable=False)
    type_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("project_types.type_id"))
    status_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("project_statuses.status_id"))
    arrangement_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("project_arrangements.arrangement_id"))
    assignment_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("project_assignments.assignment_id"))
    
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    total_days: Mapped[Optional[int]] = mapped_column(Integer)
    
    point_ach: Mapped[Optional[float]] = mapped_column(DECIMAL(10,2))
    point_req: Mapped[Optional[float]] = mapped_column(DECIMAL(10,2))
    point_percent: Mapped[Optional[float]] = mapped_column(DECIMAL(5,2))
    
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    # Relationships
    partner: Mapped["Partner"] = relationship(back_populates="projects")
    pics: Mapped[List["User"]] = relationship(secondary="project_pics")
    tasks: Mapped[List["Task"]] = relationship(back_populates="project")
    compliance_entries: Mapped[List["ComplianceEntry"]] = relationship(back_populates="project")
