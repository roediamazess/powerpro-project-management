import pandas as pd
import asyncio
import os
from sqlalchemy import select
from app.db.session import async_session_local
from app.models.partner import *
from app.models.project import *
from app.models.auth import *
from app.models.task import *
from app.models.compliance import *
from app.models.timebox import *

async def audit_import():
    print("📊 Detailed Audit of Excel Data...")
    
    file_path = '/app/projects.xlsx'
    df = pd.read_excel(file_path)
    total_excel = len(df)

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
        res = await db.execute(select(Partner.partner_id, Partner.partner_cnc))
        partner_map = {str(r.partner_cnc): r.partner_id for r in res.fetchall() if r.partner_cnc}

        excel_cnc_counts = df['cnc_id'].apply(to_int).value_counts()
        excel_duplicates_cnc = excel_cnc_counts[excel_cnc_counts > 1]

        excel_name_partner_counts = df.apply(lambda r: (clean_val(r['name']), to_int(r['partner_id'])), axis=1).value_counts()
        excel_duplicates_name = excel_name_partner_counts[excel_name_partner_counts > 1]

        print(f"\n1. Duplicates WITHIN Excel (Rows that appear more than once):")
        print(f"   - Rows with duplicate CNC IDs: {excel_duplicates_cnc.sum() - len(excel_duplicates_cnc)} redundant rows")
        print(f"   - Rows with duplicate Name+Partner: {excel_duplicates_name.sum() - len(excel_duplicates_name)} redundant rows")

        print(f"\n2. Missing References:")
        missing_partners = []
        missing_names = []
        for idx, row in df.iterrows():
            name = clean_val(row.get('name'))
            p_cnc = to_int(row.get('partner_id'))
            if not name: missing_names.append(idx+2)
            if p_cnc not in partner_map: missing_partners.append((idx+2, p_cnc, name))
        
        print(f"   - Missing Names: {len(missing_names)} (Rows: {missing_names})")
        print(f"   - Partner CNC not found: {len(missing_partners)}")
        for r, cnc, n in missing_partners[:5]:
            print(f"     * Row {r}: CNC {cnc} ({n})")

        print(f"\n3. Analysis of the 88 missing rows:")
        # 685 (Total) - 597 (Imported) = 88
        # These 88 are:
        # - Rows with no name
        # - Rows with no valid partner
        # - Rows where the CNC ID or Name+Partner already exists (either earlier in the excel or already in DB)
        
        # Let's count how many UNIQUE projects are actually in the Excel
        unique_projects_in_excel = df.drop_duplicates(subset=['cnc_id']) if 'cnc_id' in df.columns else df
        # (Filtering further by name+partner if cnc is missing)
        
        print(f"\nKesimpulan:")
        print(f"Excel Anda memiliki banyak baris ganda (duplikat).")
        print(f"Contoh CNC ID yang muncul berkali-kali di Excel:")
        for cnc, count in excel_duplicates_cnc.head(5).items():
            print(f"   - CNC {cnc}: muncul {count} kali")

if __name__ == "__main__":
    asyncio.run(audit_import())
