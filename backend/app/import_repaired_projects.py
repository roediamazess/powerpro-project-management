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

async def import_repaired_projects():
    print("🚀 Starting repaired project import...")
    
    file_path = '/app/import-projects-after-skipped.xlsx'
    if not os.path.exists(file_path):
        print(f"❌ File not found at {file_path}")
        return

    try:
        df = pd.read_excel(file_path)
        print(f"✅ Loaded {len(df)} rows from repaired Excel.")
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return

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
        # 1. Refresh Partners
        res = await db.execute(select(Partner.partner_id, Partner.partner_cnc))
        partner_map = {str(r.partner_cnc): r.partner_id for r in res.fetchall() if r.partner_cnc}
        
        # 2. Sync Lookups (Just in case)
        lookups = {
            'type_id': (ProjectType, 'type_id'),
            'status_id': (ProjectStatus, 'status_id'),
            'information_id': (ProjectInformation, 'information_id')
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

        # 3. Import
        count = 0
        for idx, row in df.iterrows():
            excel_row = row.get('Excel_Row_Number', idx + 2)
            
            # Validation
            name = clean_val(row.get('name'))
            if not name:
                print(f"❌ Row {excel_row}: SKIPPED - Project Name is still empty.")
                continue

            p_cnc = to_int_str(row.get('partner_id'))
            p_uuid = partner_map.get(p_cnc)
            if not p_uuid:
                print(f"❌ Row {excel_row}: SKIPPED - Partner CNC '{p_cnc}' still not found in DB. Please check if you added it correctly.")
                continue

            # Check for existing project to avoid double import
            cnc_id = to_int_str(row.get('cnc_id'))
            exists_query = select(Project).where(
                (Project.cnc_id == cnc_id) | 
                ((Project.name == name) & (Project.partner_id == p_uuid))
            )
            exists_res = await db.execute(exists_query)
            if exists_res.scalar_one_or_none():
                # print(f"ℹ️ Row {excel_row}: SKIPPED - Project '{name}' already exists in DB.")
                continue

            # Dates & Calculations
            start_date = parse_date(row.get('start_date'))
            end_date = parse_date(row.get('end_date'))
            handover_or = parse_date(row.get('handover_or'))
            check_or = parse_date(row.get('check_or'))
            validation_date = parse_date(row.get('validation_date'))
            s1_estimation = parse_date(row.get('s1_estimation'))

            total_days = (end_date - start_date).days + 1 if start_date and end_date else None
            
            point_ach = to_float(row.get('point_ach'))
            point_req = to_float(row.get('point_req'))
            point_percent = (point_ach / point_req) * 100 if point_req and point_req > 0 else None

            handover_days = (handover_or - end_date).days if handover_or and end_date else None
            check_days = (check_or - handover_or).days if check_or and handover_or else None
            validation_days = (validation_date - check_or).days if validation_date and check_or else None
            s1_over_days = (s1_estimation - start_date).days if s1_estimation and start_date else None

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
                "total_days": total_days,
                "point_ach": point_ach,
                "point_req": point_req,
                "point_percent": point_percent,
                "status": clean_val(row.get('status')) or "OPEN",
                "handover_or": handover_or,
                "handover_days": handover_days,
                "pic_kpi_2": to_float(row.get('pic_kpi_2')),
                "check_or": check_or,
                "check_days": check_days,
                "officer_kpi2": to_float(row.get('officer_kpi2')),
                "validation_date": validation_date,
                "validation_days": validation_days,
                "okr_kpi2": to_float(row.get('okr_kpi2')),
                "s1_estimation": s1_estimation,
                "s1_over_days": s1_over_days,
                "s1_count_email_sent": clean_val(row.get('s1_count_email_sent')),
                "s2_email_sent": clean_val(row.get('s2_email_sent')),
                "s3_email_sent": clean_val(row.get('s3_email_sent')),
                "pyear": pyear,
                "pquarter": pquarter,
                "pmonth": pmonth,
                "pweekno": pweekno,
                "pweekofmonth": pweekofmonth,
            }

            try:
                await db.execute(insert(Project).values(**project_data))
                count += 1
                print(f"✅ Row {excel_row}: Successfully imported '{name}'.")
            except Exception as e:
                print(f"❌ Row {excel_row}: FAILED to import '{name}'. Error: {e}")
        
        await db.commit()
        print(f"\n🏁 Finished. {count} additional projects added.")

if __name__ == "__main__":
    asyncio.run(import_repaired_projects())
