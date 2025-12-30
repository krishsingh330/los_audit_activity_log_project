from pydantic_settings import BaseSettings,SettingsConfigDict
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
    # Default database connection string
    DATABASE_URL: str 
    DEBUG: bool = False
    ENUM_ENCRYPTION_KEY: str = None
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    

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

