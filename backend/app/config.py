from pydantic_settings import BaseSettings
from typing import Optional
import os
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://fahmidhamim@localhost:5432/echobriefdb"
    
    # JWT
    jwt_secret: str = "your-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # AI Services
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    
    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # File Storage
    upload_dir: str = "./uploads"
    max_file_size: int = 104857600  # 100MB
    
    # Environment
    environment: str = "development"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
cors_origins = ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000"]
