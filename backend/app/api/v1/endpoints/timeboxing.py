from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.timebox import Timebox
from app.models.auth import User
from app.schemas.task import Timebox as TimeboxSchema, TimeboxCreate, TimeboxUpdate
from app.api.v1.endpoints.login import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TimeboxSchema])
async def read_timeboxes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user_id: Optional[uuid.UUID] = None,
) -> Any:
    """
    Retrieve user schedule / timeboxes. Managers can view team members.
    """
    target_user_id = current_user.user_id
    
    if user_id and user_id != current_user.user_id:
        if current_user.role_id not in ["ADMIN", "MANAGER"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view another user's schedule"
            )
        target_user_id = user_id

    stmt = (
        select(Timebox)
        .where(Timebox.user_id == target_user_id)
        .where(Timebox.is_deleted == False)
        .order_by(Timebox.start_time.asc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=TimeboxSchema)
async def create_task(
    *,
    db: AsyncSession = Depends(get_db),
    timebox_in: TimeboxCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new timeblock in calendar. Users can only create for themselves.
    """
    # Force user_id to current_user
    db_obj = Timebox(
        **timebox_in.dict(exclude={"user_id"}),
        user_id=current_user.user_id
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.patch("/{id}", response_model=TimeboxSchema)
async def update_timebox(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    timebox_in: TimeboxUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a timeblock. Users can only update their own.
    """
    stmt = select(Timebox).where(Timebox.timebox_id == id, Timebox.user_id == current_user.user_id)
    result = await db.execute(stmt)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Timebox entry not found or you don't have permission to edit it"
        )
    
    update_data = timebox_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
        
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.delete("/{id}", response_model=TimeboxSchema)
async def delete_timebox(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete a timeblock. Users can only delete their own.
    """
    stmt = select(Timebox).where(Timebox.timebox_id == id, Timebox.user_id == current_user.user_id)
    result = await db.execute(stmt)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Timebox entry not found or you don't have permission to delete it"
        )
    
    db_obj.is_deleted = True
    db.add(db_obj)
    await db.commit()
    return db_obj
