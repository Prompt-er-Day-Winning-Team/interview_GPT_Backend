import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # mysql database info
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str
    DB_USER: str
    DB_PASSWORD: str
    OPENAI_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = f"{Path(os.path.dirname(__file__)).parent.parent}/config/service.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


config = Settings()
