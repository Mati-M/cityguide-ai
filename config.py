"""
Configuration module for the application.

Loads settings from .env file and makes them available throughout the application.
Uses Pydantic for validation and type parsing.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings class.

    Automatically reads variables from .env file.

    Attributes:
        environment: Runtime environment (development/production)
        database_url: PostgreSQL connection string
        openai_api_key: API key for OpenAI services
    """

    # Runtime environment
    environment: str = "development"

    # Database
    database_url: str

    # OpenAI
    openai_api_key: str

    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


# Singleton instance - use this everywhere
settings = Settings()
