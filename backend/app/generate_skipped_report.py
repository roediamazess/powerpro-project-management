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

async def generate_skipped_report():
    print("📋 Generating report for skipped projects...")
    
    excel_path = '/app/projects.xlsx'
    output_path = '/app/skipped_projects.xlsx'
    
    df = pd.read_excel(excel_path)
    
    def clean_val(val):
        if pd.isna(val) or val is None: return None
        s = str(val).strip()
        if s.lower() in ('nan', 'none', '', 'null', 'nat'): return None
        return s

    def to_int(val):
        if pd.isna(val) or val is None: return None
        try: return str(int(float(val)))
        except: return str(val)

    async with async_session_local() as db:
        # Get existing data for mapping and duplicate checking
        p_res = await db.execute(select(Partner.partner_id, Partner.partner_cnc))
        partner_map = {str(r.partner_cnc): r.partner_id for r in p_res.fetchall() if r.partner_cnc}
        
        # We need to know which projects WERE NOT imported.
        # An easy way is to check which ones ARE in the DB now.
        # But we need to distinguish between "already imported" and "skipped due to error/missing partner".
        
        res = await db.execute(select(Project.cnc_id, Project.name, Project.partner_id))
        db_projects = res.fetchall()
        db_cnc = {str(r.cnc_id) for r in db_projects if r.cnc_id}
        db_name_partner = {(str(r.name).strip().lower(), r.partner_id) for r in db_projects}

        skipped_rows = []
        
        # Track what we see in THIS excel to detect duplicates WITHIN the file
        seen_cnc_in_this_pass = set()
        seen_name_partner_in_this_pass = set()

        for idx, row in df.iterrows():
            name = clean_val(row.get('name'))
            cnc_id = to_int(row.get('cnc_id'))
            p_cnc = to_int(row.get('partner_id'))
            p_uuid = partner_map.get(p_cnc)
            
            reason = None
            
            if not name:
                reason = "Missing Project Name"
            elif not p_uuid:
                reason = f"Partner CNC '{p_cnc}' not found in database"
            elif cnc_id:
                if cnc_id in seen_cnc_in_this_pass:
                    reason = f"Duplicate CNC ID '{cnc_id}' within Excel file"
                elif cnc_id not in db_cnc:
                    # This shouldn't happen if we just imported everything, 
                    # but maybe it was skipped for another reason.
                    reason = "Unknown Skip (Possible Data Error)"
                seen_cnc_in_this_pass.add(cnc_id)
            else:
                # No CNC ID, check by name+partner
                name_key = (name.lower().strip(), p_uuid)
                if name_key in seen_name_partner_in_this_pass:
                    reason = "Duplicate Name+Partner within Excel file"
                elif name_key not in db_name_partner:
                    reason = "Unknown Skip (Possible Data Error)"
                seen_name_partner_in_this_pass.add(name_key)

            # If it's in the DB and was NOT a duplicate in the Excel file, then it was imported.
            # If it's NOT in the DB OR it was a duplicate, it's skipped for our report.
            
            is_in_db = False
            if cnc_id and cnc_id in db_cnc: is_in_db = True
            elif name and p_uuid and (name.lower().strip(), p_uuid) in db_name_partner: is_in_db = True
            
            # If a reason was found OR it's somehow not in the DB, add to report
            if reason or not is_in_db:
                row_copy = row.copy()
                row_copy['Skip_Reason'] = reason or "Already exists in Database / Duplicate"
                row_copy['Excel_Row_Number'] = idx + 2
                skipped_rows.append(row_copy)

        if skipped_rows:
            skipped_df = pd.DataFrame(skipped_rows)
            # Reorder columns to put Reason and Row Number at the front
            cols = ['Excel_Row_Number', 'Skip_Reason'] + [c for c in skipped_df.columns if c not in ['Excel_Row_Number', 'Skip_Reason']]
            skipped_df = skipped_df[cols]
            
            skipped_df.to_excel(output_path, index=False)
            print(f"✅ Generated report with {len(skipped_df)} skipped rows at {output_path}")
        else:
            print("ℹ️ No skipped rows found.")

if __name__ == "__main__":
    asyncio.run(generate_skipped_report())
