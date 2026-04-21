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
from app.models.project import (
    ProjectType, ProjectStatus, ProjectArrangement, ProjectAssignment, ProjectInformation
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

@router.get("/project")
async def get_project_lookups(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get all lookup data for project forms and settings."""
    types = (await db.execute(select(ProjectType).order_by(ProjectType.listindex))).scalars().all()
    statuses = (await db.execute(select(ProjectStatus).order_by(ProjectStatus.listindex))).scalars().all()
    arrangements = (await db.execute(select(ProjectArrangement).order_by(ProjectArrangement.listindex))).scalars().all()
    assignments = (await db.execute(select(ProjectAssignment).order_by(ProjectAssignment.listindex))).scalars().all()
    information = (await db.execute(select(ProjectInformation).order_by(ProjectInformation.listindex))).scalars().all()

    return {
        "types": [{"id": x.type_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in types],
        "statuses": [{"id": x.status_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in statuses],
        "arrangements": [{"id": x.arrangement_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in arrangements],
        "assignments": [{"id": x.assignment_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in assignments],
        "information": [{"id": x.information_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in information],
    }

@router.get("/user")
async def get_user_lookups(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get roles and tiers for user management."""
    from app.models.auth import Role, Tier
    roles = (await db.execute(select(Role).order_by(Role.listindex))).scalars().all()
    tiers = (await db.execute(select(Tier).order_by(Tier.listindex))).scalars().all()

    return {
        "roles": [{"id": x.role_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in roles],
        "tiers": [{"id": x.tier_id, "name": x.name, "listindex": x.listindex, "is_active": x.is_active} for x in tiers],
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

# PROJECT TYPES
@router.post("/project-types", response_model=Lookup)
async def create_project_type(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, ProjectType, "type_id", schema)

@router.put("/project-types/{id_val}", response_model=Lookup)
async def update_project_type(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, ProjectType, "type_id", id_val, schema)

# PROJECT STATUSES
@router.post("/project-statuses", response_model=Lookup)
async def create_project_status(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, ProjectStatus, "status_id", schema)

@router.put("/project-statuses/{id_val}", response_model=Lookup)
async def update_project_status(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, ProjectStatus, "status_id", id_val, schema)

# PROJECT ARRANGEMENTS
@router.post("/project-arrangements", response_model=Lookup)
async def create_project_arrangement(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, ProjectArrangement, "arrangement_id", schema)

@router.put("/project-arrangements/{id_val}", response_model=Lookup)
async def update_project_arrangement(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, ProjectArrangement, "arrangement_id", id_val, schema)

# PROJECT ASSIGNMENTS
@router.post("/project-assignments", response_model=Lookup)
async def create_project_assignment(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, ProjectAssignment, "assignment_id", schema)

@router.put("/project-assignments/{id_val}", response_model=Lookup)
async def update_project_assignment(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, ProjectAssignment, "assignment_id", id_val, schema)

# PROJECT INFORMATION
@router.post("/project-information", response_model=Lookup)
async def create_project_information(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await create_lookup(db, ProjectInformation, "information_id", schema)

@router.put("/project-information/{id_val}", response_model=Lookup)
async def update_project_information(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    return await update_lookup(db, ProjectInformation, "information_id", id_val, schema)

# USER ROLES
@router.post("/roles", response_model=Lookup)
async def create_role(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    from app.models.auth import Role
    return await create_lookup(db, Role, "role_id", schema)

@router.put("/roles/{id_val}", response_model=Lookup)
async def update_role(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    from app.models.auth import Role
    return await update_lookup(db, Role, "role_id", id_val, schema)

# USER TIERS
@router.post("/tiers", response_model=Lookup)
async def create_tier(schema: LookupCreate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    from app.models.auth import Tier
    return await create_lookup(db, Tier, "tier_id", schema)

@router.put("/tiers/{id_val}", response_model=Lookup)
async def update_tier(id_val: str, schema: LookupUpdate, db: AsyncSession = Depends(get_db), u: User = Depends(get_current_user)):
    from app.models.auth import Tier
    return await update_lookup(db, Tier, "tier_id", id_val, schema)

