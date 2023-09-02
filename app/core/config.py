import os
from pathlib import Path

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # mysql database info
    db_host: str
    db_port: int
    db_database: str
    db_user: str
    db_password: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = f'{Path(os.path.dirname(__file__)).parent.parent}/config/service.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False

config = Settings()

