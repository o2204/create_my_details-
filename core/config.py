from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    
    SUPABASE_URL: str
    SUPABASE_KEY: str 

    COHERE_API_KEY: str 

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()