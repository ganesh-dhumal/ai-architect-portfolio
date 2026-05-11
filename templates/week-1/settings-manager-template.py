"""Environment configuration manager for AI engineering systems."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application configuration."""

    APP_NAME: str = "AI Engineering Platform"
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)

    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)

    LOG_LEVEL: str = Field(default="INFO")

    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None

    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/ai_platform"
    )

    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    VECTOR_DB_PROVIDER: str = Field(default="qdrant")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()


if __name__ == "__main__":
    settings = get_settings()

    print(f"Application: {settings.APP_NAME}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Vector Database: {settings.VECTOR_DB_PROVIDER}")
