from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from db.engine import engine

AsyncSessionLocal = async_sessionmaker(
    bind=engine, # use the async engine (PostgreSQL)
    class_=AsyncSession, # create async sessions
    expire_on_commit=False, # data won't be expired after commit
)

async def get_db(): 
    async with AsyncSessionLocal() as session:
        yield session