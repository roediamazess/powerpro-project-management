from typing import Any, Dict, List, Type
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.base import Base
from app.db.session import get_db
from app.models.partner import (
    PartnerType, PartnerStatus, PartnerGroup, PartnerArea, 
    PartnerSubArea, PartnerSystemVersion, PartnerImplementationType
)
from app.schemas.lookups import (
    Lookup, LookupCreate, LookupUpdate,
    SubArea, SubAreaCreate, SubAreaUpdate
)
from app.api.v1.endpoints.login import get_current_user
from app.models.auth import User

router = APIRouter()

# Mapping of table names to models and schemas for generic routing if needed, 
# but for clarity and type safety we'll define explicit routes.

@router.get("/partner")
async def get_partner_lookups(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get all lookup data for partner forms."""
    types = (await db.execute(select(PartnerType).order_by(PartnerType.listindex))).scalars().all()
    statuses = (await db.execute(select(PartnerStatus).order_by(PartnerStatus.listindex))).scalars().all()
    groups = (await db.execute(select(PartnerGroup).order_by(PartnerGroup.listindex))).scalars().all()
    areas = (await db.execute(select(PartnerArea).order_by(PartnerArea.listindex))).scalars().all()
    sub_areas = (await db.execute(select(PartnerSubArea).order_by(PartnerSubArea.listindex))).scalars().all()
    versions = (await db.execute(select(PartnerSystemVersion).order_by(PartnerSystemVersion.listindex))).scalars().all()
    imp_types = (await db.execute(select(PartnerImplementationType).order_by(PartnerImplementationType.listindex))).scalars().all()

    return {
        "types": [{"id": x.type_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in types],
        "statuses": [{"id": x.status_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in statuses],
        "groups": [{"id": x.group_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in groups],
        "areas": [{"id": x.area_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in areas],
        "sub_areas": [{"id": x.sub_area_id, "name": x.name, "area_id": x.area_id, "listindex": x.listindex, "is_active": x.is_active} for x in sub_areas],
        "versions": [{"id": x.version_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in versions],
        "imp_types": [{"id": x.imp_type_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in imp_types],
    }

# --- Generic CRUD Helper Logic ---

from sqlalchemy.exc import IntegrityError

async def create_lookup(db: AsyncSession, model: Type[Base], id_attr: str, schema: LookupCreate):
    try:
        obj = model(**{id_attr: schema.id, "name": schema.name, "listindex": schema.listindex, "is_active": schema.is_active})
        db.add(obj)
        await db.commit()
        return {"id": getattr(obj, id_attr), "name": obj.name, "listindex": obj.listindex, "is_active": obj.is_active}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with ID '{schema.id}' already exists."
        )

async def update_lookup(db: AsyncSession, model: Type[Base], id_attr: str, id_val: str, schema: LookupUpdate):
    result = await db.execute(select(model).where(getattr(model, id_attr) == id_val))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = schema.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)
    
    await db.commit()
    return {"id": getattr(obj, id_attr), "name": obj.name, "listindex": obj.listindex, "is_active": obj.is_active}

async def delete_lookup(db: AsyncSession, model: Type[Base], id_attr: str, id_val: str):
    result = await db.execute(select(model).where(getattr(model, id_attr) == id_val))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(obj)
    await db.commit()
    return {"message": "Deleted successfully"}

# --- EXPLICIT ROUTES FOR SETTINGS ---

# PARTNER TYPES
@router.post("/partner-types", response_model=Lookup)
async def create_partner_type(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, PartnerType, "type_id", schema)

@router.put("/partner-types/{id_val}", response_model=Lookup)
async def update_partner_type(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, PartnerType, "type_id", id_val, schema)

# PARTNER STATUSES
@router.post("/partner-statuses", response_model=Lookup)
async def create_partner_status(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, PartnerStatus, "status_id", schema)

@router.put("/partner-statuses/{id_val}", response_model=Lookup)
async def update_partner_status(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, PartnerStatus, "status_id", id_val, schema)

# PARTNER GROUPS
@router.post("/partner-groups", response_model=Lookup)
async def create_partner_group(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, PartnerGroup, "group_id", schema)

@router.put("/partner-groups/{id_val}", response_model=Lookup)
async def update_partner_group(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, PartnerGroup, "group_id", id_val, schema)

# PARTNER AREAS
@router.post("/partner-areas", response_model=Lookup)
async def create_partner_area(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, PartnerArea, "area_id", schema)

@router.put("/partner-areas/{id_val}", response_model=Lookup)
async def update_partner_area(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, PartnerArea, "area_id", id_val, schema)

# PARTNER SUB-AREAS
@router.post("/partner-sub-areas", response_model=SubArea)
async def create_partner_sub_area(schema: SubAreaCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    try:
        obj = PartnerSubArea(sub_area_id=schema.id, name=schema.name, area_id=schema.area_id, listindex=schema.listindex, is_active=schema.is_active)
        db.add(obj)
        await db.commit()
        return {"id": obj.sub_area_id, "name": obj.name, "area_id": obj.area_id, "listindex": obj.listindex, "is_active": obj.is_active}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sub-Area with ID '{schema.id}' already exists."
        )

@router.put("/partner-sub-areas/{id_val}", response_model=SubArea)
async def update_partner_sub_area(id_val: str, schema: SubAreaUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    result = await db.execute(select(PartnerSubArea).where(PartnerSubArea.sub_area_id == id_val))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = schema.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)
    
    await db.commit()
    return {"id": obj.sub_area_id, "name": obj.name, "area_id": obj.area_id, "listindex": obj.listindex, "is_active": obj.is_active}

# PARTNER VERSIONS
@router.post("/partner-versions", response_model=Lookup)
async def create_partner_version(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, PartnerSystemVersion, "version_id", schema)

@router.put("/partner-versions/{id_val}", response_model=Lookup)
async def update_partner_version(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, PartnerSystemVersion, "version_id", id_val, schema)

# PARTNER IMPLEMENTATION TYPES
@router.post("/partner-imp-types", response_model=Lookup)
async def create_partner_imp_type(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, PartnerImplementationType, "imp_type_id", schema)

@router.put("/partner-imp-types/{id_val}", response_model=Lookup)
async def update_partner_imp_type(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, PartnerImplementationType, "imp_type_id", id_val, schema)
