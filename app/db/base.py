"""
Database base configuration.

Sets up SQLAlchemy core components and imports all models.
"""

from sqlalchemy.ext.declarative import declarative_base

# Base class for all database models
Base = declarative_base()

# Import all models so they are registered with SQLAlchemy
from app.models import place  # noqa
