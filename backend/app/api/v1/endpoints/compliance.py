from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.compliance import ComplianceForm, ComplianceItem, ComplianceEntry, ComplianceEntryScore
from app.models.auth import User
from app.schemas.compliance import (
    ComplianceForm as FormSchema,
    ComplianceEntryRead, 
    ComplianceEntryCreate
)
from app.api.v1.endpoints.login import get_current_user

router = APIRouter()

# --- Forms Management (Admin/Manager) ---

@router.get("/forms", response_model=List[FormSchema])
async def read_forms(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve active compliance forms with their items.
    """
    stmt = select(ComplianceForm).where(ComplianceForm.is_active == True).options(selectinload(ComplianceForm.items))
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/forms", response_model=FormSchema)
async def create_form(
    *,
    db: AsyncSession = Depends(get_db),
    form_in: Any, # Using Any for quick prototype, should use schema in prod
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create a new compliance form template. Admin only.
    """
    if current_user.role_id != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can create forms")
    
    db_obj = ComplianceForm(
        **form_in,
        created_by=current_user.user_id,
        updated_by=current_user.user_id
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.post("/items", response_model=Any)
async def create_item(
    *,
    db: AsyncSession = Depends(get_db),
    item_in: Any,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create a new audit item. Admin only.
    """
    if current_user.role_id != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can create items")
    
    db_obj = ComplianceItem(
        **item_in,
        created_by=current_user.user_id,
        updated_by=current_user.user_id
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

# --- Entries & Scoring Logic ---

@router.get("/entries", response_model=List[ComplianceEntryRead])
async def read_entries(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 1000,
) -> Any:
    """
    Retrieve compliance audit entries with improvement calculation.
    """
    stmt = (
        select(ComplianceEntry)
        .where(ComplianceEntry.is_deleted == False)
        .options(
            selectinload(ComplianceEntry.form),
            selectinload(ComplianceEntry.scores).selectinload(ComplianceEntryScore.item)
        )
        .order_by(ComplianceEntry.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    entries = result.scalars().all()
    
    # Batch lookup baseline scores
    baseline_ids = [e.baseline_id for e in entries if e.baseline_id]
    if baseline_ids:
        stmt_baselines = select(ComplianceEntry.entry_id, ComplianceEntry.compliance_percent).where(ComplianceEntry.entry_id.in_(baseline_ids))
        res_baselines = await db.execute(stmt_baselines)
        baseline_map = {row[0]: row[1] for row in res_baselines.all()}
        
        for e in entries:
            if e.baseline_id and e.baseline_id in baseline_map:
                e.improvement_percent = e.compliance_percent - baseline_map[e.baseline_id]
            else:
                e.improvement_percent = 0.0
    else:
        for e in entries:
            e.improvement_percent = 0.0
            
    return entries

@router.post("/entries", response_model=ComplianceEntryRead)
async def create_entry(
    *,
    db: AsyncSession = Depends(get_db),
    entry_in: ComplianceEntryCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Submit an audit entry and calculate weighted score.
    """
    # 0. Fetch Weights for the selected form items
    stmt_weights = select(ComplianceFormItem).where(ComplianceFormItem.form_id == entry_in.form_id)
    res_weights = await db.execute(stmt_weights)
    weights_map = {w.item_id: w.weight for w in res_weights.scalars().all()}

    # 1. Initialize entry
    db_obj = ComplianceEntry(
        **entry_in.dict(exclude={"scores"}),
        agent_id=current_user.user_id,
        created_by=current_user.user_id,
        updated_by=current_user.user_id
    )
    
    # 2. Add individual scores & apply weights
    total_weighted_score = 0
    max_weighted_possible = 0
    
    for s in entry_in.scores:
        weight = weights_map.get(s.item_id, 1) # Fallback to 1
        score_obj = ComplianceEntryScore(
            item_id=s.item_id,
            score=s.score,
            remark=s.remark,
            photo_url=s.photo_url
        )
        db_obj.scores.append(score_obj)
        total_weighted_score += (s.score * weight)
        max_weighted_possible += (5 * weight)
        
    # 3. Calculate metrics
    db_obj.score_metric = float(total_weighted_score)
    db_obj.score_max = float(max_weighted_possible)
    if max_weighted_possible > 0:
        db_obj.compliance_percent = (total_weighted_score / max_weighted_possible) * 100
    else:
        db_obj.compliance_percent = 0
        
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    # Reload with all relations for response
    stmt = select(ComplianceEntry).where(ComplianceEntry.entry_id == db_obj.entry_id).options(
        selectinload(ComplianceEntry.form),
        selectinload(ComplianceEntry.scores).selectinload(ComplianceEntryScore.item)
    )
    result = await db.execute(stmt)
    return result.scalar_one()

@router.get("/entries/{id}", response_model=ComplianceEntryRead)
async def read_entry(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get audit entry detail.
    """
    stmt = (
        select(ComplianceEntry)
        .where(ComplianceEntry.entry_id == id)
        .options(
            selectinload(ComplianceEntry.form),
            selectinload(ComplianceEntry.scores).selectinload(ComplianceEntryScore.item)
        )
    )
    result = await db.execute(stmt)
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Audit entry not found")
    return entry
