"""
Main module of the CityGuide AI application.

Initializes FastAPI application and defines endpoints.
"""

from enum import Enum

from fastapi import FastAPI

from app.api.endpoints import places
from config import settings


class Environment(str, Enum):
    development = "development"
    production = "production"


environment = Environment(settings.environment)

# Initialize FastAPI application
app = FastAPI(
    title="CityGuide AI",
    description="Intelligent city guide powered by AI",
    version="0.1.0",
    debug=(settings.environment == environment.development),
)

# Register routers
app.include_router(places.router, prefix="/api/v1", tags=["places"])


@app.get("/")
async def root() -> dict:
    """
    Root endpoint. Checks if the API is alive.

    Returns:
        dict: Welcome message and environment information
    """
    return {
        "message": "CityGuide AI is running!",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint. Used by monitoring systems and load balancers.

    Returns:
        dict: Application status and version
    """
    return {"status": "healthy", "api_version": "0.1.0"}
