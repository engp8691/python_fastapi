# ALLOWED_ORIGINS=http://localhost:3000,https://yourfrontend.com
# DATABASE_URL=postgresql+asyncpg://cradl:cradl@localhost:5432/cradl
# DATABASE_URL_SYNC=postgresql+psycopg2://cradl:cradl@localhost:5432/cradl
# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session
