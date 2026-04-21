from typing import Any, List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.task import Task
from app.models.auth import User
from app.schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate
from app.api.v1.endpoints.login import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TaskSchema])
async def read_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 1000,
) -> Any:
    """
    Retrieve project tasks.
    """
    stmt = (
        select(Task)
        .where(Task.is_deleted == False)
        .options(selectinload(Task.project))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=TaskSchema)
async def create_task(
    *,
    db: AsyncSession = Depends(get_db),
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new task.
    """
    db_obj = Task(
        **task_in.dict(),
        created_by=current_user.user_id,
        updated_by=current_user.user_id
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    # Reload with project
    stmt = select(Task).where(Task.task_id == db_obj.task_id).options(selectinload(Task.project))
    result = await db.execute(stmt)
    return result.scalar_one()

@router.patch("/{id}", response_model=TaskSchema)
async def update_task(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    task_in: TaskUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a task.
    """
    stmt = select(Task).where(Task.task_id == id, Task.is_deleted == False)
    result = await db.execute(stmt)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
        
    db_obj.updated_by = current_user.user_id
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    # Reload with project
    stmt = select(Task).where(Task.task_id == id).options(selectinload(Task.project))
    result = await db.execute(stmt)
    return result.scalar_one()

@router.delete("/{id}", response_model=TaskSchema)
async def delete_task(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Soft-delete a task.
    """
    stmt = select(Task).where(Task.task_id == id, Task.is_deleted == False)
    result = await db.execute(stmt)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_obj.is_deleted = True
    db.add(db_obj)
    await db.commit()
    return db_obj
