"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "AI Sustainable Cities Planner"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/sustainable_cities"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # API Keys (for external data sources)
    OPENWEATHER_API_KEY: Optional[str] = None
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    EPA_API_KEY: Optional[str] = None
    
    # Simulation
    SIMULATION_MAX_AGENTS: int = 10000
    SIMULATION_TIMESTEPS: int = 1000
    SIMULATION_PARALLEL_WORKERS: int = 4
    
    # ML Models
    MODEL_CACHE_SIZE: int = 100
    MODEL_UPDATE_INTERVAL: int = 3600  # seconds
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
