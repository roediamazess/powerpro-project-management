import sys
import os
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import select, insert, text
from app.db.session import async_session_local
from app.models.partner import *
from app.models.project import *
from app.models.task import *
from app.models.auth import *
from app.models.compliance import *
from app.models.audit import *
from app.models.timebox import *

async def import_partners():
    print("🚀 Starting partner import process...")
    
    # 1. Read Excel
    try:
        df = pd.read_excel('/app/partners.xlsx')
        print(f"✅ Loaded {len(df)} rows from Excel.")
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return

    # Helper function to clean values VERY aggressively
    def clean_val(val):
        if pd.isna(val) or val is None: return None
        s = str(val).strip()
        if s.lower() in ('nan', 'none', '', 'null', '<null>', 'undefined'): return None
        return s

    # Clean the entire dataframe
    for col in df.columns:
        df[col] = df[col].apply(clean_val)
    
    # Mapping for outlet -> outlets
    if 'outlet' in df.columns and 'outlets' not in df.columns:
        df = df.rename(columns={'outlet': 'outlets'})

    async with async_session_local() as db:
        async with db.begin():
            # 2. Sync Lookups
            lookups = {
                'type_id': (PartnerType, 'type_id'),
                'status_id': (PartnerStatus, 'status_id'),
                'group_id': (PartnerGroup, 'group_id'),
                'area_id': (PartnerArea, 'area_id'),
                'version_id': (PartnerSystemVersion, 'version_id'),
                'imp_type_id': (PartnerImplementationType, 'imp_type_id')
            }

            for col, (model, id_field) in lookups.items():
                if col in df.columns:
                    unique_ids = df[col].dropna().unique()
                    for uid in unique_ids:
                        uid = str(uid).strip()
                        if uid == '': continue
                        q = select(model).where(getattr(model, id_field) == uid)
                        res = await db.execute(q)
                        if not res.scalar_one_or_none():
                            print(f"➕ Adding missing lookup: {col} -> {uid}")
                            await db.execute(insert(model).values({id_field: uid, "name": uid}))

            # Special case for sub_area
            if 'sub_area_id' in df.columns:
                unique_subs = df[['sub_area_id', 'area_id']].dropna().drop_duplicates()
                for _, row in unique_subs.iterrows():
                    sid = clean_val(row['sub_area_id'])
                    aid = clean_val(row['area_id'])
                    if not sid or not aid: continue
                    q = select(PartnerSubArea).where(PartnerSubArea.sub_area_id == sid)
                    res = await db.execute(q)
                    if not res.scalar_one_or_none():
                        print(f"➕ Adding missing sub_area: {sid} (Area: {aid})")
                        await db.execute(insert(PartnerSubArea).values(sub_area_id=sid, area_id=aid, name=sid))

            # 3. Import Partners
            count = 0
            for _, row in df.iterrows():
                def parse_date(val):
                    c = clean_val(val)
                    if not c: return None
                    try:
                        # Try common formats
                        s_val = str(c).strip()
                        for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y'):
                            try:
                                return datetime.strptime(s_val, fmt)
                            except:
                                continue
                        return pd.to_datetime(s_val)
                    except:
                        return None

                def to_int(val):
                    c = clean_val(val)
                    if not c: return None
                    try:
                        return int(float(c))
                    except:
                        return None

                partner_data = {
                    "partner_cnc": clean_val(row['partner_cnc']),
                    "name": clean_val(row['name']),
                    "type_id": clean_val(row['type_id']),
                    "status_id": clean_val(row['status_id']),
                    "group_id": clean_val(row['group_id']),
                    "area_id": clean_val(row['area_id']),
                    "sub_area_id": clean_val(row['sub_area_id']),
                    "version_id": clean_val(row['version_id']),
                    "imp_type_id": clean_val(row['imp_type_id']),
                    "stars": to_int(row['stars']),
                    "rooms": to_int(row['rooms']),
                    "outlets": to_int(row['outlets']),
                    "address": clean_val(row['address']),
                    "system_live_at": parse_date(row['system_live_at']),
                    "last_visit_at": parse_date(row['last_visit_at']),
                    "last_visit_type": clean_val(row['last_visit_type']),
                    "last_project": parse_date(row['last_project']),
                    "last_project_type": clean_val(row['last_project_type']),
                    "is_active": True if str(row['is_active']).lower() in ('1', 'true', 'yes') else False
                }

                if not partner_data['name']: continue

                # Check for existing by Name
                exists_query = select(Partner).where(Partner.name == partner_data['name'])
                exists_res = await db.execute(exists_query)
                if not exists_res.scalar_one_or_none():
                    await db.execute(insert(Partner).values(**partner_data))
                    count += 1
            
            print(f"🏁 Import finished. {count} new partners added.")

if __name__ == "__main__":
    asyncio.run(import_partners())
