import pandas as pd
import asyncio
import os
from sqlalchemy import select
from app.db.session import async_session_local
from app.models.partner import *
from app.models.project import *
from app.models.task import *
from app.models.auth import *
from app.models.compliance import *
from app.models.timebox import *

async def final_audit():
    print("📋 Final Audit: Original Excel (685) vs Database (600)")
    
    file_path = '/app/projects.xlsx'
    df = pd.read_excel(file_path)
    
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
        # 1. Get Partners
        p_res = await db.execute(select(Partner.partner_id, Partner.partner_cnc))
        partner_map = {str(r.partner_cnc): r.partner_id for r in p_res.fetchall() if r.partner_cnc}
        
        # 2. Get All Projects in DB
        res = await db.execute(select(Project.cnc_id, Project.name, Project.partner_id))
        db_rows = res.fetchall()
        db_cnc = {str(r.cnc_id) for r in db_rows if r.cnc_id}
        db_name_partner = {(str(r.name).strip().lower(), r.partner_id) for r in db_rows}

        skipped_data = []
        
        # Track what we processed from Excel to detect duplicates WITHIN the Excel
        processed_in_this_run_cnc = set()
        processed_in_this_run_name_partner = set()

        for idx, row in df.iterrows():
            name = clean_val(row.get('name'))
            cnc_id = to_int_str(row.get('cnc_id'))
            p_cnc = to_int_str(row.get('partner_id'))
            p_uuid = partner_map.get(p_cnc)
            
            is_in_db = False
            if cnc_id and cnc_id in db_cnc: is_in_db = True
            elif name and p_uuid and (name.lower().strip(), p_uuid) in db_name_partner: is_in_db = True
            
            if is_in_db:
                # This project is already in DB.
                # However, is THIS specific row a duplicate of another row in the SAME excel?
                if cnc_id:
                    if cnc_id in processed_in_this_run_cnc:
                        skipped_data.append({
                            "Row": idx + 2,
                            "CNC_ID": cnc_id,
                            "Project_Name": name,
                            "Reason": "DUPLICATE: CNC ID ini sudah muncul di baris sebelumnya dalam Excel."
                        })
                    processed_in_this_run_cnc.add(cnc_id)
                elif name and p_uuid:
                    name_key = (name.lower().strip(), p_uuid)
                    if name_key in processed_in_this_run_name_partner:
                        skipped_data.append({
                            "Row": idx + 2,
                            "CNC_ID": cnc_id,
                            "Project_Name": name,
                            "Reason": "DUPLICATE: Kombinasi Nama + Partner ini sudah muncul di baris sebelumnya."
                        })
                    processed_in_this_run_name_partner.add(name_key)
                continue
            
            # If NOT in DB, why?
            reason = "Unknown Error"
            if not name:
                reason = "DATA ERROR: Nama project kosong (Mandatory)."
            elif not p_uuid:
                reason = f"DATA ERROR: Partner CNC '{p_cnc}' tidak ditemukan di tabel Partners."
            else:
                reason = "DATA ERROR: Terjadi kesalahan saat proses import (cek format data)."

            skipped_data.append({
                "Row": idx + 2,
                "CNC_ID": cnc_id,
                "Project_Name": name,
                "Reason": reason
            })

        print(f"\nAudit Results: {len(skipped_data)} rows not imported from original 685.")
        
        # Export to CSV for user to see
        out_df = pd.DataFrame(skipped_data)
        out_df.to_excel('/app/final_missing_report.xlsx', index=False)
        print(f"✅ Final report saved to /app/final_missing_report.xlsx")

if __name__ == "__main__":
    asyncio.run(final_audit())
