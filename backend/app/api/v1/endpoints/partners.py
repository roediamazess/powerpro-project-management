from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.partner import Partner, PartnerContact
from app.schemas.partner import Partner as PartnerSchema, PartnerCreate, PartnerUpdate
from app.api.v1.endpoints.login import get_current_user
from app.models.auth import User

router = APIRouter()

@router.get("/", response_model=List[PartnerSchema])
async def read_partners(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve partners.
    """
    stmt = (
        select(Partner)
        .where(Partner.is_deleted == False)
        .options(selectinload(Partner.contacts))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=PartnerSchema)
async def create_partner(
    *,
    db: AsyncSession = Depends(get_db),
    partner_in: PartnerCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new partner.
    """
    # 1. Create Partner
    db_obj = Partner(
        **partner_in.dict(exclude={"contacts"}),
        created_by=current_user.user_id,
        updated_by=current_user.user_id
    )
    db.add(db_obj)
    await db.flush() # Get partner_id
    
    # 2. Add Contacts if any
    if partner_in.contacts:
        for contact_in in partner_in.contacts:
            contact = PartnerContact(
                **contact_in.dict(),
                partner_id=db_obj.partner_id
            )
            db.add(contact)
    
    await db.commit()
    await db.refresh(db_obj)
    
    # Reload with contacts
    stmt = select(Partner).where(Partner.partner_id == db_obj.partner_id).options(selectinload(Partner.contacts))
    result = await db.execute(stmt)
    return result.scalar_one()

@router.get("/{id}", response_model=PartnerSchema)
async def read_partner(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get partner by ID.
    """
    stmt = select(Partner).where(Partner.partner_id == id, Partner.is_deleted == False).options(selectinload(Partner.contacts))
    result = await db.execute(stmt)
    partner = result.scalar_one_or_none()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner

@router.patch("/{id}", response_model=PartnerSchema)
async def update_partner(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    partner_in: PartnerUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a partner.
    """
    stmt = select(Partner).where(Partner.partner_id == id, Partner.is_deleted == False)
    result = await db.execute(stmt)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    update_data = partner_in.dict(exclude_unset=True, exclude={"contacts"})
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    # Handle Contacts if provided
    if partner_in.contacts is not None:
        # Delete existing
        await db.execute(delete(PartnerContact).where(PartnerContact.partner_id == id))
        # Add new
        for contact_in in partner_in.contacts:
            contact = PartnerContact(
                **contact_in.dict(),
                partner_id=id
            )
            db.add(contact)

    db_obj.updated_by = current_user.user_id
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    # Reload with contacts
    stmt = select(Partner).where(Partner.partner_id == id).options(selectinload(Partner.contacts))
    result = await db.execute(stmt)
    return result.scalar_one()

@router.delete("/{id}", response_model=PartnerSchema)
async def delete_partner(
    *,
    db: AsyncSession = Depends(get_db),
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Soft-delete a partner.
    """
    stmt = select(Partner).where(Partner.partner_id == id, Partner.is_deleted == False)
    result = await db.execute(stmt)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    db_obj.is_deleted = True
    db_obj.deleted_at = datetime.utcnow()
    db.add(db_obj)
    await db.commit()
    return db_obj
