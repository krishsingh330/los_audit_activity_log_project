from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
class Settings(BaseSettings):
    """
    Application configuration settings.
    
    Attributes:
        DATABASE_URL (str): The database connection string.
        DEBUG (bool): Debug mode flag.
    """
    # Default database connection string (should be overridden by env vars in production)
    # Default database connection string (should be overridden by env vars in production)
    DATABASE_URL: str 
    DEBUG: bool = False
    ENUM_ENCRYPTION_KEY: str = None

    class Config:
        """
        Pydantic settings configuration.
        Reads variables from a .env file.
        """
        env_file = BASE_DIR/".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of the settings.
    
    Using lru_cache ensures that the settings are only loaded once from the environment/file
    and then reused, improving performance.
    
    Returns:
        Settings: The application settings object.
    """
    return Settings()

