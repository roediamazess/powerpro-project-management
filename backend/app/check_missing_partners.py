import pandas as pd
import asyncio
from sqlalchemy import select
from app.db.session import async_session_local
from app.models.partner import *
from app.models.project import *
from app.models.task import *
from app.models.auth import *
from app.models.compliance import *

async def check():
    try:
        df = pd.read_excel('/app/projects.xlsx')
        # Clean excel_ids to handle .0 from floats
        excel_ids = set()
        for val in df['partner_id'].dropna():
            try:
                s_val = str(int(float(val)))
                excel_ids.add(s_val)
            except:
                excel_ids.add(str(val))
        
        async with async_session_local() as db:
            res = await db.execute(select(Partner.partner_cnc))
            db_ids = set(str(r[0]) for r in res.fetchall() if r[0] is not None)
            
            missing = excel_ids - db_ids
            if missing:
                print(f"⚠️ Missing {len(missing)} partner_cnc in DB: {sorted(list(missing))[:10]}...")
            else:
                print("✅ All partners in Excel found in DB.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
