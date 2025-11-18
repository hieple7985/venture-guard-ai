from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    API_VERSION: str = "v1"
    
    DATABASE_URL: str = "sqlite:///./ventureguard.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    OPENAI_API_KEY: str = ""
    HAVEIBEENPWNED_API_KEY: str = ""
    VIRUSTOTAL_API_KEY: str = ""
    
    WEB3_PROVIDER_URL: str = ""
    CONTRACT_ADDRESS: str = ""
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
