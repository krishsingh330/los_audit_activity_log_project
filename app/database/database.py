from sqlmodel import SQLModel, create_engine, Session
from app.core.config import get_settings
import os

# Load application settings
settings = get_settings()

# Determine Database URL
# Uses environment variable if present, otherwise falls back to settings default
DATABASE_URL = settings.DATABASE_URL

# Create Database Engine
# This engine manages the connection pool to the database.
engine = create_engine(
    DATABASE_URL,
    echo=False # Set to True to see raw SQL queries in logs
)

# Dependency for FastAPI (if needed, though dependencies.py is preferred)
def get_db():
    """
    Generator function to provide a database session.
    
    Yields:
        Session: A SQLModel session connected to the database.
    """
    with Session(engine) as session:
        yield session
