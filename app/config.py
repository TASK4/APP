import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "DoAnLTANTT"
    SECRET_KEY: str = os.getenv("SECRET_KEY", r"oiKIbInKqtLzlIStcMVOLPKgtpiBgDut_roLl5Yl9XI")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()