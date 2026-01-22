from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from core.config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, ##### are this correct? or put in main.py!!!!!!
    echo=False, # SQLAlchemy does NOT print SQL queries
)
