import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Intermediation Platform"
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changethisinvproduction")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours

    def validate_setup(self):
        if not self.SUPABASE_URL or "AQUI" in self.SUPABASE_URL:
            raise ValueError("SUPABASE_URL is not set properly in .env")
        if not self.SUPABASE_KEY or "AQUI" in self.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY is not set properly in .env")

settings = Settings()
