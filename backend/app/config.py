import os
from typing import List, Union
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production-0982347209384")

    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    API_BASE_URL: str = Field(default="http://localhost:8000")
    WEBSOCKET_URL: str = Field(default="ws://localhost:8000/api/v1/ws/operations")

    # DB Connection
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/dost_guardian"
    )
    DB_POOL_SIZE: int = Field(default=10)
    DB_MAX_OVERFLOW: int = Field(default=20)

    # Redis Connection
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    # Security & CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
