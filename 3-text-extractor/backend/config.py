import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_HOST: str = os.getenv("DB_HOST")

    class Config:
        env_file = ".env"


settings = Settings()
