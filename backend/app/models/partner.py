import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, PowerProBase

class Partner(Base, PowerProBase):
    __tablename__ = "partners"

    partner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    partner_cnc: Mapped[Optional[str]] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    website: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Relationships
    area_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("partner_areas.area_id"))
    sub_area_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("partner_sub_areas.sub_area_id"))
    type_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("partner_types.type_id"))
    status_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("partner_statuses.status_id"))
    group_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("partner_groups.group_id"))
    version_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("partner_system_versions.version_id"))
    imp_type_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("partner_implementation_types.imp_type_id"))

    # Operational Metrics
    stars: Mapped[Optional[int]] = mapped_column(Integer)
    rooms: Mapped[Optional[int]] = mapped_column(Integer)
    outlets: Mapped[Optional[int]] = mapped_column(Integer)
    system_live_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Recent Activity
    last_visit_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_visit_type: Mapped[Optional[str]] = mapped_column(String)
    last_project: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_project_type: Mapped[Optional[str]] = mapped_column(String)


    is_active: Mapped[bool] = mapped_column(default=True)

    
    # Bi-directional relationships
    contacts: Mapped[List["PartnerContact"]] = relationship(back_populates="partner")
    projects: Mapped[List["Project"]] = relationship(back_populates="partner")

class PartnerContact(Base, PowerProBase):

    __tablename__ = "partner_contacts"

    contact_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    partner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("partners.partner_id"))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    position: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    partner: Mapped["Partner"] = relationship(back_populates="contacts")

class PartnerArea(Base):
    __tablename__ = "partner_areas"
    area_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

class PartnerSubArea(Base):
    __tablename__ = "partner_sub_areas"
    sub_area_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    area_id: Mapped[str] = mapped_column(String(50), ForeignKey("partner_areas.area_id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

class PartnerGroup(Base):
    __tablename__ = "partner_groups"
    group_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

class PartnerType(Base):
    __tablename__ = "partner_types"
    type_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

class PartnerStatus(Base):
    __tablename__ = "partner_statuses"
    status_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

class PartnerSystemVersion(Base):
    __tablename__ = "partner_system_versions"
    version_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

class PartnerImplementationType(Base):
    __tablename__ = "partner_implementation_types"
    imp_type_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    listindex: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
