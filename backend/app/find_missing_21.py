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

async def find_missing_21():
    print("🔍 Searching for the 21 missing projects...")
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
        
        res = await db.execute(select(Project.cnc_id, Project.name, Project.partner_id))
        db_rows = res.fetchall()
        db_cnc = {str(r.cnc_id) for r in db_rows if r.cnc_id}
        db_name_partner = {(str(r.name).strip().lower(), r.partner_id) for r in db_rows}

        missing = []
        seen_cnc = set()
        
        for idx, row in df.iterrows():
            name = clean_val(row.get('name'))
            cnc_id = to_int_str(row.get('cnc_id'))
            p_cnc = to_int_str(row.get('partner_id'))
            p_uuid = partner_map.get(p_cnc)
            
            if not cnc_id: continue
            if cnc_id in seen_cnc: continue # Skip redundancy within excel
            seen_cnc.add(cnc_id)
            
            if cnc_id not in db_cnc:
                # Why is this CNC ID not in DB?
                reason = "Unknown"
                if not name:
                    reason = "Nama Project Kosong"
                elif not p_uuid:
                    reason = f"Partner CNC {p_cnc} Tidak Ditemukan"
                elif (name.lower().strip(), p_uuid) in db_name_partner:
                    reason = f"Nama Project + Partner sudah ada di DB (dengan CNC ID lain)"
                else:
                    reason = "Alasan lain (Data Error)"
                
                missing.append({
                    "Row": idx + 2,
                    "CNC_ID": cnc_id,
                    "Name": name,
                    "Reason": reason
                })

        print(f"Total Missing Unique CNC IDs: {len(missing)}")
        for m in missing:
            print(f"  - Row {m['Row']}: CNC {m['CNC_ID']} ({m['Name']}) -> {m['Reason']}")

if __name__ == "__main__":
    asyncio.run(find_missing_21())
