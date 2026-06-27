import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "healthycare_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password_lo")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    # Gemini API Settings
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

settings = Config()