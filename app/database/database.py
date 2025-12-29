from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

# Load application settings
settings = get_settings()

# Determine Database URL
# Uses environment variable if present, otherwise falls back to settings default
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL:
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    elif DATABASE_URL.startswith("postgresql+asyncpg://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)

# Create Database Engine
# This engine manages the connection pool to the database.
# Using echo=False for production readiness, can be set to True for debugging
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# Dependency for FastAPI (if needed, though dependencies.py is preferred)
async def get_db():
    """
    Generator function to provide an asynchronous database session.
    
    Yields:
        AsyncSession: A SQLModel async session connected to the database.
    """
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
