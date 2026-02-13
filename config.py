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
        openai_api_key: API key for OpenAI services
        environment: Runtime environment (development/production)
    """

    # OpenAI (placeholder for now - will be used later)
    openai_api_key: str

    # Runtime environment
    environment: str = "development"

    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


# Singleton instance - use this everywhere
settings = Settings()
