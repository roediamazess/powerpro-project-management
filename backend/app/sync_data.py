import asyncio
import sys
import os

# Add parent directory to sys.path to allow imports from 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.db.session import async_session_local

# Import EVERYTHING to avoid mapper errors
from app.models.auth import User, Role, Tier
from app.models.partner import Partner, PartnerContact, PartnerArea, PartnerSubArea, PartnerType, PartnerStatus, PartnerSystemVersion, PartnerImplementationType, PartnerServerInformation
from app.models.project import Project, ProjectPIC, ProjectType, ProjectStatus, ProjectArrangement, ProjectAssignment, ProjectInformation
from app.models.task import Task, TaskStatus, TaskPriority, TaskDepartment
from app.models.compliance import ComplianceForm, ComplianceItem, ComplianceEntry, ComplianceEntryScore, ComplianceFormItem
from app.models.timebox import Timebox
from app.models.audit import SystemAuditLog

# Define categories
VISIT_TYPES = ['IMPLEMENTATION', 'UPGRADE', 'MAINTENANCE', 'RE-TRAINING', 'IH-TRAINING', 'SPEC-REQ']
PROJECT_TYPES = ['REMOTE-INS', 'OL-TRAINING', 'OTH']

async def sync_partners_from_projects():
    async with async_session_local() as db:
        # 1. Fetch all partners
        result = await db.execute(select(Partner))
        partners = result.scalars().all()
        
        print(f"Syncing {len(partners)} partners...")
        
        for partner in partners:
            # --- LAST VISIT ---
            visit_stmt = (
                select(Project)
                .where(Project.partner_id == partner.partner_id)
                .where(Project.type_id.in_(VISIT_TYPES))
                .order_by(Project.start_date.desc())
                .limit(1)
            )
            v_res = await db.execute(visit_stmt)
            last_visit_proj = v_res.scalar_one_or_none()
            
            if last_visit_proj:
                if not partner.last_visit_at or last_visit_proj.start_date > partner.last_visit_at:
                    partner.last_visit_at = last_visit_proj.start_date
                    partner.last_visit_type = last_visit_proj.type_id
                    print(f"Updated Visit for {partner.name}: {last_visit_proj.start_date}")

            # --- LAST PROJECT ---
            proj_stmt = (
                select(Project)
                .where(Project.partner_id == partner.partner_id)
                .where(Project.type_id.in_(PROJECT_TYPES))
                .order_by(Project.start_date.desc())
                .limit(1)
            )
            p_res = await db.execute(proj_stmt)
            last_proj_proj = p_res.scalar_one_or_none()
            
            if last_proj_proj:
                if not partner.last_project or last_proj_proj.start_date > partner.last_project:
                    partner.last_project = last_proj_proj.start_date
                    partner.last_project_type = last_proj_proj.type_id
                    print(f"Updated Project for {partner.name}: {last_proj_proj.start_date}")
        
        await db.commit()
        print("Sync complete.")

if __name__ == "__main__":
    asyncio.run(sync_partners_from_projects())
