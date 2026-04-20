import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base, PowerProBase

class TaskPriority(Base):
    __tablename__ = "task_priorities"
    priority_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    listindex: Mapped[int] = mapped_column(default=0)

class TaskStatus(Base):
    __tablename__ = "task_statuses"
    status_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    listindex: Mapped[int] = mapped_column(default=0)

class TaskDepartment(Base):
    __tablename__ = "task_departments"
    dept_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    listindex: Mapped[int] = mapped_column(default=0)

class Task(Base, PowerProBase):
    __tablename__ = "tasks"
    
    task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_no: Mapped[Optional[str]] = mapped_column(String(20))
    
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.project_id"))
    partner_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("partners.partner_id"))
    
    priority_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("task_priorities.priority_id"))
    status_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("task_statuses.status_id"))
    dept_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("task_departments.dept_id"))
    
    assignee_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    action_solution: Mapped[Optional[str]] = mapped_column(Text)
    
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="tasks")
    assignee: Mapped["User"] = relationship(foreign_keys=[assignee_id])
    timeboxes: Mapped[list["Timebox"]] = relationship(back_populates="task")
