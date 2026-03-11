from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Nexus Sports API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    
    # Storage
    DATA_DIR: str = Field("data", env="DATA_DIR")
    ARCHIVE_DIR: str = Field("data/archived_files", env="ARCHIVE_DIR")
    
    # Database
    DATABASE_URL: str = Field("sqlite:///./data/nexus_sports.db", env="DATABASE_URL")
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.ARCHIVE_DIR, exist_ok=True)
