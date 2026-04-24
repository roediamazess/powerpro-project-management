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

async def audit_project_pics():
    print("📊 Auditing Project PIC Assignments...")
    
    file_path = '/app/projects-pic.xlsx'
    output_path = '/app/skipped_project_pics.xlsx'
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
        # Get Projects
        res = await db.execute(select(Project.project_id, Project.cnc_id, Project.name))
        projects = res.fetchall()
        project_map = {str(r.cnc_id): r.project_id for r in projects if r.cnc_id}
        project_names = {str(r.cnc_id): r.name for r in projects if r.cnc_id}
        
        # Get Users
        res = await db.execute(select(User.user_id, User.username))
        user_map = {str(r.username).lower(): r.user_id for r in res.fetchall()}

        skipped_rows = []

        for idx, row in df.iterrows():
            cnc_id = to_int_str(row.get('cnc_id'))
            username = clean_val(row.get('user_id'))
            
            reason = None
            if not project_map.get(cnc_id):
                reason = f"Project dengan CNC ID '{cnc_id}' tidak ditemukan di database (Kemungkinan duplikat/konflik nama di tahap sebelumnya)."
            elif not username:
                reason = "Username (PIC) kosong di Excel."
            elif username.lower() not in user_map:
                reason = f"User dengan username '{username}' tidak ditemukan di database."
            
            if reason:
                row_copy = row.copy()
                row_copy['Excel_Row_Number'] = idx + 2
                row_copy['Skip_Reason'] = reason
                skipped_rows.append(row_copy)

        if skipped_rows:
            skipped_df = pd.DataFrame(skipped_rows)
            # Reorder columns
            cols = ['Excel_Row_Number', 'Skip_Reason'] + [c for c in skipped_df.columns if c not in ['Excel_Row_Number', 'Skip_Reason']]
            skipped_df = skipped_df[cols]
            
            skipped_df.to_excel(output_path, index=False)
            print(f"✅ Generated report with {len(skipped_df)} skipped rows at {output_path}")
        else:
            print("ℹ️ No skipped rows found.")

if __name__ == "__main__":
    asyncio.run(audit_project_pics())
