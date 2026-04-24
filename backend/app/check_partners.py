import asyncio
from sqlalchemy import text
from app.db.session import async_session_local

async def check():
    async with async_session_local() as db:
        res = await db.execute(text("SELECT partner_id, partner_cnc, name FROM partners LIMIT 5"))
        print(res.fetchall())

if __name__ == "__main__":
    asyncio.run(check())
