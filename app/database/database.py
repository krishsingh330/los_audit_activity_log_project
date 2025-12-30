from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

# Load application settings
settings = get_settings()

# Determine Database URL
DATABASE_URL = settings.DATABASE_URL
DATABASE_URL = DATABASE_URL.replace(
    "postgresql://",
    "postgresql+asyncpg://",
    1
)

# Create Database Engine
engine = create_async_engine(
    DATABASE_URL,
)



