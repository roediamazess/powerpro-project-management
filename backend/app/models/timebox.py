import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base, PowerProBase

class Timebox(Base, PowerProBase):
    __tablename__ = "timeboxing"
    
    timebox_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    
    task_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.task_id"))
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.project_id"))
    
    activity_name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    color_code: Mapped[Optional[str]] = mapped_column(String(20)) # e.g., 'cyan', 'emerald'
    
    is_completed: Mapped[bool] = mapped_column(default=False)

    # Relationships
    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    task: Mapped["Task"] = relationship(back_populates="timeboxes")
    project: Mapped["Project"] = relationship()
