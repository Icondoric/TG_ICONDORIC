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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # ML Model (Fase 6)
    ML_MODEL_PATH: str = os.getenv("ML_MODEL_PATH", "app/ml/trained_models/ridge_v1.joblib")
    ML_MODEL_VERSION: str = os.getenv("ML_MODEL_VERSION", "v1")

    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MAX_RETRIES: int = int(os.getenv("GEMINI_MAX_RETRIES", "3"))

    # File Upload
    MAX_CV_FILE_SIZE_MB: int = int(os.getenv("MAX_CV_FILE_SIZE_MB", "10"))
    ALLOWED_CV_EXTENSIONS: str = os.getenv("ALLOWED_CV_EXTENSIONS", "pdf")

    # Cache
    PROFILE_CACHE_TTL_SECONDS: int = int(os.getenv("PROFILE_CACHE_TTL_SECONDS", "300"))

    def validate_setup(self):
        if not self.SUPABASE_URL or "AQUI" in self.SUPABASE_URL:
            raise ValueError("SUPABASE_URL is not set properly in .env")
        if not self.SUPABASE_KEY or "AQUI" in self.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY is not set properly in .env")

    def validate_gemini(self):
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in .env")


settings = Settings()
