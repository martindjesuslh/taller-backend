from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DATABASE
    DB_HOST: str
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ADA Restauraciones"

    # SECURITY
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ENVIRONMENT
    ENVIRONMENT: Literal["dev", "prod"] = "dev"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
