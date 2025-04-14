# app/db/create_tables.py
import asyncio
from app.db.database import engine
from app.db.models.orm_models import Base

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_all())
