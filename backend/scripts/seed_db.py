import asyncio
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.session import async_session_local
from app.core import security
from app.models.auth import User, Role, Tier
from app.models.partner import PartnerType, PartnerStatus, PartnerGroup, PartnerArea, PartnerSubArea, Partner
from app.models.project import ProjectType, ProjectStatus, ProjectArrangement, Project
from app.models.task import TaskPriority, TaskStatus, TaskDepartment, Task
from app.models.timebox import Timebox
from app.models.compliance import ComplianceItem, ComplianceForm

async def seed_data():
    async with async_session_local() as session:
        print("Starting Database Seeding (v2.1 Standard)...")
        
        # 1. ROLES
        roles = [
            {"role_id": "ADMIN", "name": "Administrator", "description": "Full System Access"},
            {"role_id": "MANAGER", "name": "Manager", "description": "Escalation & Monitoring"},
            {"role_id": "OFFICER", "name": "Field Officer", "description": "Compliance & Projects"},
            {"role_id": "VIEWER", "name": "Viewer", "description": "Read-Only Access"},
        ]
        for r in roles:
            stmt = select(Role).where(Role.role_id == r["role_id"])
            existing = (await session.execute(stmt)).scalar_one_or_none()
            if not existing:
                session.add(Role(**r))
        
        # 2. TIERS
        tiers = [
            {"tier_id": "T1", "name": "Silver"},
            {"tier_id": "T2", "name": "Gold"},
            {"tier_id": "T3", "name": "Platinum"},
        ]
        for t in tiers:
            stmt = select(Tier).where(Tier.tier_id == t["tier_id"])
            existing = (await session.execute(stmt)).scalar_one_or_none()
            if not existing:
                session.add(Tier(**t))

        # 3. SUPERUSER
        admin_stmt = select(User).where(User.username == "admin")
        admin_user = (await session.execute(admin_stmt)).scalar_one_or_none()
        if not admin_user:
            admin_user = User(
                user_id=uuid.uuid4(),
                username="admin",
                fullname="PowerPro Admin",
                email="admin@powerpro.id",
                password_hash=security.get_password_hash("admin"),
                role_id="ADMIN",
                tier_id="T3",
                is_active=True
            )
            session.add(admin_user)
            print("Superuser 'admin' created (PW: admin)")

        # 4. PARTNER MASTER
        p_types = ["HOTEL", "RESORT", "VILLA", "RESTO"]
        for pt in p_types:
            stmt = select(PartnerType).where(PartnerType.type_id == pt)
            if not (await session.execute(stmt)).scalar_one_or_none():
                session.add(PartnerType(type_id=pt, name=pt.capitalize()))

        p_statuses = ["ACTIVE", "INACTIVE", "BLACKLIST"]
        for ps in p_statuses:
            stmt = select(PartnerStatus).where(PartnerStatus.status_id == ps)
            if not (await session.execute(stmt)).scalar_one_or_none():
                session.add(PartnerStatus(status_id=ps, name=ps.capitalize()))

        # 5. PROJECT MASTER
        proj_statuses = ["PLANNING", "IN_PROGRESS", "COMPLETED", "ON_HOLD"]
        for prs in proj_statuses:
            stmt = select(ProjectStatus).where(ProjectStatus.status_id == prs)
            if not (await session.execute(stmt)).scalar_one_or_none():
                session.add(ProjectStatus(status_id=prs, name=prs.replace('_', ' ').capitalize()))

        # 6. TASK MASTER
        task_priorities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        for tp in task_priorities:
            stmt = select(TaskPriority).where(TaskPriority.priority_id == tp)
            if not (await session.execute(stmt)).scalar_one_or_none():
                session.add(TaskPriority(priority_id=tp, name=tp.capitalize()))

        await session.commit() # Commit master data before reference data
        
        # Start new transaction for reference data
        async with async_session_local() as session:
            # 7. SAMPLE PARTNER
            sample_partner_id = uuid.uuid4()
            partner_stmt = select(Partner).where(Partner.name == "Grand Mulia Bali")
            if not (await session.execute(partner_stmt)).scalar_one_or_none():
                sample_partner = Partner(
                    partner_id=sample_partner_id,
                    name="Grand Mulia Bali",
                    partner_cnc="H-001",
                    rooms=150,
                    stars=5,
                    type_id="HOTEL",
                    status_id="ACTIVE"
                )
                session.add(sample_partner)

                # 8. SAMPLE PROJECT
                sample_project = Project(
                    project_id=uuid.uuid4(),
                    name="PMS Installation & Setup",
                    partner_id=sample_partner_id,
                    status_id="IN_PROGRESS",
                    start_date=datetime.utcnow()
                )
                session.add(sample_project)

            await session.commit()
            print("Seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
