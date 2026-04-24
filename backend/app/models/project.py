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

class ProjectInformation(Base):
    __tablename__ = "project_information"
    information_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

# --- Junction Table ---
class ProjectPIC(Base):
    __tablename__ = "project_pics"
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.project_id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    arrangement_id: Mapped[str] = mapped_column(String(50), default="SELF")
    assignment_id: Mapped[str] = mapped_column(String(50), default="SELF")
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    total_days: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default="OPEN")
    
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)

    project: Mapped["Project"] = relationship(back_populates="pic_assignments")
    user: Mapped["User"] = relationship()

# --- Main Tables ---
class Project(Base, PowerProBase):
    __tablename__ = "projects"
    
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cnc_id: Mapped[Optional[str]] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    partner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("partners.partner_id"), nullable=False)
    type_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("project_types.type_id"))
    status_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("project_statuses.status_id"))
    information_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("project_information.information_id"))
    
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    total_days: Mapped[Optional[int]] = mapped_column(Integer)
    
    point_ach: Mapped[Optional[float]] = mapped_column(DECIMAL(10,2))
    point_req: Mapped[Optional[float]] = mapped_column(DECIMAL(10,2))
    point_percent: Mapped[Optional[float]] = mapped_column(DECIMAL(5,2))
    status: Mapped[str] = mapped_column(String(20), default="OPEN")

    # Extended Fields
    handover_or: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    handover_days: Mapped[Optional[int]] = mapped_column(Integer)
    pic_kpi_2: Mapped[Optional[float]] = mapped_column(DECIMAL(10,2))
    
    check_or: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    check_days: Mapped[Optional[int]] = mapped_column(Integer)
    officer_kpi2: Mapped[Optional[float]] = mapped_column(DECIMAL(10,2))
    
    validation_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    validation_days: Mapped[Optional[int]] = mapped_column(Integer)
    okr_kpi2: Mapped[Optional[float]] = mapped_column(DECIMAL(10,2))
    
    s1_estimation: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    s1_over_days: Mapped[Optional[int]] = mapped_column(Integer)
    s1_count_email_sent: Mapped[Optional[str]] = mapped_column(String(255))
    s2_email_sent: Mapped[Optional[str]] = mapped_column(String(255))
    s3_email_sent: Mapped[Optional[str]] = mapped_column(String(255))
    
    pyear: Mapped[Optional[int]] = mapped_column(Integer)
    pquarter: Mapped[Optional[str]] = mapped_column(String(20))
    pmonth: Mapped[Optional[str]] = mapped_column(String(20))
    pweekno: Mapped[Optional[str]] = mapped_column(String(20))
    pweekofmonth: Mapped[Optional[str]] = mapped_column(String(20))
    
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    # Relationships
    partner: Mapped["Partner"] = relationship(back_populates="projects")
    pic_assignments: Mapped[List["ProjectPIC"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    pics: Mapped[List["User"]] = relationship(secondary="project_pics", viewonly=True)
    tasks: Mapped[List["Task"]] = relationship(back_populates="project")
    compliance_entries: Mapped[List["ComplianceEntry"]] = relationship(back_populates="project")
    training_sessions: Mapped[List["ORTrainingSession"]] = relationship(back_populates="project")
