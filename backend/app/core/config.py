import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Basic app settings
    app_name: str = "Relevantic Recall"
    debug: bool = False
    
    # Database
    database_url: str = os.getenv("DATABASE_URL")
    
    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OAuth2 Google
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    
    # OAuth2 GitHub
    github_client_id: str = os.getenv("GITHUB_CLIENT_ID", "")
    github_client_secret: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    
    # Frontend URL for redirects
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

settings = Settings()