from typing import Any, List, Optional
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.project import Project, ProjectPIC
from app.models.partner import Partner
from app.models.auth import User
from app.schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate
from app.api.v1.endpoints.login import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProjectSchema])
async def read_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 1000,
) -> Any:
    """
    Retrieve projects with partners and pics.
    """
    stmt = (
        select(Project)
        .where(Project.is_deleted == False)
        .options(
            selectinload(Project.partner),
            selectinload(Project.pic_assignments).selectinload(ProjectPIC.user)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    projects = result.scalars().all()
    
    # Custom mapping for PICs to include additional info from User table
    # In a real project, we'd use a more complex join or property in the model
    return projects

@router.post("/", response_model=ProjectSchema)
async def create_project(
    *,
    db: AsyncSession = Depends(get_db),
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new project and assign PICs.
    """
    # 1. Create Project
    db_obj = Project(
        **project_in.dict(exclude={"pic_assignments"}),
        created_by=current_user.user_id,
        updated_by=current_user.user_id
    )
    
    # Calculate total days if dates provided
    if db_obj.start_date and db_obj.end_date:
        db_obj.total_days = (db_obj.end_date - db_obj.start_date).days + 1
        
    db.add(db_obj)
    await db.flush()
    
    # 2. Add PICs
    if project_in.pic_assignments:
        for pa in project_in.pic_assignments:
            pic = ProjectPIC(
                project_id=db_obj.project_id,
                **pa.dict()
            )
            db.add(pic)
            
    await db.commit()
    await db.refresh(db_obj)
    
    # Reload with relations
    stmt = select(Project).where(Project.project_id == db_obj.project_id).options(
        selectinload(Project.partner),
        selectinload(Project.pic_assignments).selectinload(ProjectPIC.user)
    )
    result = await db.execute(stmt)
    return result.scalar_one()

@router.get("/{id}", response_model=ProjectSchema)
async def read_project(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get project by ID.
    """
    stmt = select(Project).where(Project.project_id == id, Project.is_deleted == False).options(
        selectinload(Project.partner),
        selectinload(Project.pic_assignments).selectinload(ProjectPIC.user)
    )
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.patch("/{id}", response_model=ProjectSchema)
async def update_project(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    project_in: ProjectUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a project and its PICs.
    """
    stmt = select(Project).where(Project.project_id == id, Project.is_deleted == False)
    result = await db.execute(stmt)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_in.dict(exclude_unset=True, exclude={"pic_assignments"})
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    # Recalculate days
    if db_obj.start_date and db_obj.end_date:
        db_obj.total_days = (db_obj.end_date - db_obj.start_date).days + 1
        
    db_obj.updated_by = current_user.user_id
    
    # Update PICs if provided
    if project_in.pic_assignments is not None:
        # Clear existing
        await db.execute(delete(ProjectPIC).where(ProjectPIC.project_id == id))
        # Add new
        for pa in project_in.pic_assignments:
            pic = ProjectPIC(
                project_id=id, 
                **pa.dict()
            )
            db.add(pic)
            
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    # Reload with relations
    stmt = select(Project).where(Project.project_id == id).options(
        selectinload(Project.partner),
        selectinload(Project.pic_assignments).selectinload(ProjectPIC.user)
    )
    result = await db.execute(stmt)
    return result.scalar_one()

@router.delete("/{id}", response_model=ProjectSchema)
async def delete_project(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Soft-delete a project.
    """
    stmt = select(Project).where(Project.project_id == id, Project.is_deleted == False)
    result = await db.execute(stmt)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db_obj.is_deleted = True
    db_obj.deleted_at = datetime.utcnow()
    db.add(db_obj)
    await db.commit()
    return db_obj
