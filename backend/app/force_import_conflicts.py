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

async def force_import_conflicts():
    print("🚀 Starting Force Import of conflicted projects...")
    
    projects_file = '/app/projects.xlsx'
    pics_file = '/app/projects-pic.xlsx'
    
    df_p = pd.read_excel(projects_file)
    df_pic = pd.read_excel(pics_file)

    def clean_val(val):
        if pd.isna(val) or val is None: return None
        s = str(val).strip()
        if s.lower() in ('nan', 'none', '', 'null', 'nat'): return None
        return s

    def to_float(val):
        c = clean_val(val)
        if not c: return None
        try: return float(c)
        except: return None

    def to_int_str(val):
        f = to_float(val)
        return str(int(f)) if f is not None else None

    def parse_date(val):
        if pd.isna(val) or val is None: return None
        dt = None
        if isinstance(val, datetime): dt = val
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
                if not dt: dt = pd.to_datetime(s_val).to_pydatetime()
            except: return None
        if dt and dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
        return dt

    async with async_session_local() as db:
        # 1. Map Partners & Users
        res_p = await db.execute(select(Partner.partner_id, Partner.partner_cnc))
        partner_map = {str(r.partner_cnc): r.partner_id for r in res_p.fetchall() if r.partner_cnc}
        
        res_u = await db.execute(select(User.user_id, User.username))
        user_map = {str(r.username).lower(): r.user_id for r in res_u.fetchall()}

        # 2. Get Existing CNCs in DB
        res_e = await db.execute(select(Project.cnc_id))
        existing_cncs = {str(r.cnc_id) for r in res_e.fetchall() if r.cnc_id}

        # 3. Import Projects (Only if CNC_ID is missing)
        print("🔨 Importing Projects that were previously skipped due to name conflict...")
        projects_added = 0
        for idx, row in df_p.iterrows():
            cnc_id = to_int_str(row.get('cnc_id'))
            if not cnc_id or cnc_id in existing_cncs:
                continue
            
            name = clean_val(row.get('name'))
            p_cnc = to_int_str(row.get('partner_id'))
            p_uuid = partner_map.get(p_cnc)
            
            if not name or not p_uuid:
                continue

            # This is a missing CNC ID! Let's import it.
            start_date = parse_date(row.get('start_date'))
            end_date = parse_date(row.get('end_date'))
            point_ach = to_float(row.get('point_ach'))
            point_req = to_float(row.get('point_req'))
            
            pyear, pquarter, pmonth, pweekno, pweekofmonth = None, None, None, None, None
            if start_date:
                pyear = start_date.year
                pquarter = f"Q{(start_date.month - 1) // 3 + 1}"
                pmonth = start_date.strftime('%B')
                pweekno = f"Week {start_date.isocalendar()[1]}"
                pweekofmonth = f"Week {(start_date.day - 1) // 7 + 1}"

            project_data = {
                "cnc_id": cnc_id,
                "name": name,
                "partner_id": p_uuid,
                "type_id": clean_val(row.get('type_id')),
                "status_id": clean_val(row.get('status_id')),
                "information_id": clean_val(row.get('information_id')),
                "start_date": start_date,
                "end_date": end_date,
                "total_days": (end_date - start_date).days + 1 if start_date and end_date else None,
                "point_ach": point_ach,
                "point_req": point_req,
                "point_percent": (point_ach / point_req) * 100 if point_req and point_req > 0 else None,
                "status": clean_val(row.get('status')) or "OPEN",
                "handover_or": parse_date(row.get('handover_or')),
                "check_or": parse_date(row.get('check_or')),
                "validation_date": parse_date(row.get('validation_date')),
                "pyear": pyear, "pquarter": pquarter, "pmonth": pmonth, "pweekno": pweekno, "pweekofmonth": pweekofmonth,
                "s1_count_email_sent": clean_val(row.get('s1_count_email_sent')),
                "s2_email_sent": clean_val(row.get('s2_email_sent')),
                "s3_email_sent": clean_val(row.get('s3_email_sent')),
            }

            try:
                await db.execute(insert(Project).values(**project_data))
                projects_added += 1
                existing_cncs.add(cnc_id) # Add to set to avoid duplicates within this excel
                # print(f"✅ Imported project CNC {cnc_id}: {name}")
            except Exception as e:
                print(f"❌ Failed CNC {cnc_id}: {e}")
        
        await db.commit()
        print(f"✅ Total {projects_added} missing projects added.")

        # 4. Import PICs for these new projects
        print("🔨 Importing PICs for the newly added projects...")
        # Refresh project map
        res_m = await db.execute(select(Project.project_id, Project.cnc_id))
        project_map = {str(r.cnc_id): r.project_id for r in res_m.fetchall() if r.cnc_id}
        
        pics_added = 0
        for idx, row in df_pic.iterrows():
            cnc_id = to_int_str(row.get('cnc_id'))
            username = clean_val(row.get('user_id'))
            p_uuid = project_map.get(cnc_id)
            u_uuid = user_map.get(username.lower()) if username else None
            
            if not p_uuid or not u_uuid: continue

            # Check if exists
            exists_q = select(ProjectPIC).where(ProjectPIC.project_id == p_uuid, ProjectPIC.user_id == u_uuid)
            res_ex = await db.execute(exists_q)
            if res_ex.scalar_one_or_none(): continue

            start_date = parse_date(row.get('start_date'))
            end_date = parse_date(row.get('end_date'))
            
            pic_data = {
                "project_id": p_uuid, "user_id": u_uuid,
                "arrangement_id": clean_val(row.get('arrangement_id')) or "SELF",
                "assignment_id": clean_val(row.get('assignment_id')) or "SELF",
                "start_date": start_date, "end_date": end_date,
                "total_days": (end_date - start_date).days + 1 if start_date and end_date else None,
                "status": clean_val(row.get('status')) or "OPEN",
                "is_active": True, "assigned_at": datetime.now(timezone.utc)
            }
            try:
                await db.execute(insert(ProjectPIC).values(**pic_data))
                pics_added += 1
            except Exception as e:
                print(f"❌ Failed PIC for CNC {cnc_id}: {e}")
        
        await db.commit()
        print(f"✅ Total {pics_added} new PIC assignments added.")
        print("🏁 Operation complete.")

if __name__ == "__main__":
    asyncio.run(force_import_conflicts())
