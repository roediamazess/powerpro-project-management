import pandas as pd
import asyncio
import os
from datetime import datetime, timezone
from sqlalchemy import select, insert
from app.db.session import async_session_local
from app.models.partner import *
from app.models.project import *
from app.models.task import *
from app.models.auth import *
from app.models.compliance import *
from app.models.timebox import *

async def import_project_pics():
    print("🚀 Starting project PIC import process...")
    
    file_path = '/app/projects-pic.xlsx'
    if not os.path.exists(file_path):
        print(f"❌ File not found at {file_path}")
        return

    try:
        df = pd.read_excel(file_path)
        print(f"✅ Loaded {len(df)} rows from Excel.")
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return

    def clean_val(val):
        if pd.isna(val) or val is None: return None
        s = str(val).strip()
        if s.lower() in ('nan', 'none', '', 'null', 'nat'): return None
        return s

    def to_int_str(val):
        if pd.isna(val) or val is None: return None
        try: return str(int(float(val)))
        except: return str(val)

    def parse_date(val):
        if pd.isna(val) or val is None: return None
        dt = None
        if isinstance(val, datetime): 
            dt = val
        else:
            c = clean_val(val)
            if not c: return None
            try:
                s_val = str(c).strip()
                for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y'):
                    try: 
                        dt = datetime.strptime(s_val, fmt)
                        break
                    except: continue
                if not dt:
                    dt = pd.to_datetime(s_val).to_pydatetime()
            except:
                return None
        
        if dt and dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    async with async_session_local() as db:
        # 1. Map CNC ID to Project UUID
        print("🔍 Mapping projects...")
        res = await db.execute(select(Project.project_id, Project.cnc_id))
        project_map = {str(r.cnc_id): r.project_id for r in res.fetchall() if r.cnc_id}
        
        # 2. Map Username to User UUID
        print("🔍 Mapping users...")
        res = await db.execute(select(User.user_id, User.username))
        user_map = {str(r.username).lower(): r.user_id for r in res.fetchall()}

        # 3. Sync Lookups
        lookups = {
            'arrangement_id': (ProjectArrangement, 'arrangement_id'),
            'assignment_id': (ProjectAssignment, 'assignment_id')
        }

        for col, (model, id_field) in lookups.items():
            if col in df.columns:
                unique_ids = df[col].dropna().unique()
                for uid in unique_ids:
                    uid = str(uid).strip()
                    if not uid: continue
                    q = select(model).where(getattr(model, id_field) == uid)
                    res = await db.execute(q)
                    if not res.scalar_one_or_none():
                        print(f"➕ Adding missing lookup: {col} -> {uid}")
                        await db.execute(insert(model).values({id_field: uid, "name": uid}))
        await db.commit()

        # 4. Import PICs
        print("📥 Importing PIC assignments...")
        count = 0
        skipped_count = 0
        
        for idx, row in df.iterrows():
            cnc_id = to_int_str(row.get('cnc_id'))
            username = clean_val(row.get('user_id')) # In sample, user_id column has usernames
            
            p_uuid = project_map.get(cnc_id)
            u_uuid = user_map.get(username.lower()) if username else None
            
            if not p_uuid:
                print(f"⚠️ Row {idx+2}: Project CNC '{cnc_id}' not found. Skipping.")
                skipped_count += 1
                continue
            
            if not u_uuid:
                print(f"⚠️ Row {idx+2}: User '{username}' not found. Skipping.")
                skipped_count += 1
                continue

            start_date = parse_date(row.get('start_date'))
            end_date = parse_date(row.get('end_date'))
            total_days = (end_date - start_date).days + 1 if start_date and end_date else None

            pic_data = {
                "project_id": p_uuid,
                "user_id": u_uuid,
                "arrangement_id": clean_val(row.get('arrangement_id')) or "SELF",
                "assignment_id": clean_val(row.get('assignment_id')) or "SELF",
                "start_date": start_date,
                "end_date": end_date,
                "total_days": total_days,
                "status": clean_val(row.get('status')) or "OPEN",
                "is_active": True,
                "assigned_at": datetime.now(timezone.utc)
            }

            # Check if assignment already exists
            exists_query = select(ProjectPIC).where(
                ProjectPIC.project_id == pic_data['project_id'],
                ProjectPIC.user_id == pic_data['user_id']
            )
            exists_res = await db.execute(exists_query)
            if not exists_res.scalar_one_or_none():
                await db.execute(insert(ProjectPIC).values(**pic_data))
                count += 1
            
            if count % 100 == 0 and count > 0:
                print(f"⏳ Processed {count} assignments...")

        await db.commit()
        print(f"🏁 Finished. {count} PIC assignments added. {skipped_count} skipped.")

if __name__ == "__main__":
    asyncio.run(import_project_pics())
