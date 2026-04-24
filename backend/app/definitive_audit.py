import pandas as pd
import asyncio
from sqlalchemy import select
from app.db.session import async_session_local
from app.models.partner import *
from app.models.project import *
from app.models.task import *
from app.models.auth import *
from app.models.compliance import *
from app.models.timebox import *

async def definitive_audit():
    excel_path = '/app/projects.xlsx'
    df = pd.read_excel(excel_path)
    
    def clean_val(val):
        if pd.isna(val) or val is None: return None
        s = str(val).strip()
        if s.lower() in ('nan', 'none', '', 'null', 'nat'): return None
        return s

    def to_int_str(val):
        if pd.isna(val) or val is None: return None
        try: return str(int(float(val)))
        except: return str(val)

    async with async_session_local() as db:
        p_res = await db.execute(select(Partner.partner_id, Partner.partner_cnc))
        partner_map = {str(r.partner_cnc): r.partner_id for r in p_res.fetchall() if r.partner_cnc}
        
        # Get DB projects
        res = await db.execute(select(Project.cnc_id, Project.name, Project.partner_id))
        db_projects = res.fetchall()
        db_cnc = {str(r.cnc_id) for r in db_projects if r.cnc_id}
        db_name_partner = {(str(r.name).strip().lower(), r.partner_id) for r in db_projects}

        missing_rows = []
        for idx, row in df.iterrows():
            name = clean_val(row.get('name'))
            cnc_id = to_int_str(row.get('cnc_id'))
            p_cnc = to_int_str(row.get('partner_id'))
            p_uuid = partner_map.get(p_cnc)
            
            # Is this row in the DB?
            in_db = False
            if cnc_id and cnc_id in db_cnc: in_db = True
            elif name and p_uuid and (name.lower().strip(), p_uuid) in db_name_partner: in_db = True
            
            if not in_db:
                reason = "Unknown"
                if not name: reason = "Empty Project Name"
                elif not p_uuid: reason = f"Partner CNC '{p_cnc}' not found"
                else: reason = "Import Error / Logic Skip"
                
                missing_rows.append({
                    "Excel_Row": idx + 2,
                    "CNC_ID": cnc_id,
                    "Project_Name": name,
                    "Partner_CNC": p_cnc,
                    "Reason": reason
                })
        
        # Now we check why they are missing if they ARE duplicates in Excel
        # But wait, if they are NOT in DB, they are missing.
        # If they ARE in DB, they are NOT missing.
        
        print(f"Definitive Missing Count: {len(missing_rows)}")
        pd.DataFrame(missing_rows).to_excel('/app/final_audit_report_v2.xlsx', index=False)

if __name__ == "__main__":
    asyncio.run(definitive_audit())
