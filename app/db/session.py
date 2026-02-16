"""
Database session management.

Creates and manages database connections.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# Create database engine
# Engine is the starting point for any SQLAlchemy application
engine = create_engine(
    settings.database_url,
    echo=True,  # Logs all SQL queries (useful for development)
)

# SessionLocal is a factory for database sessions
# Each session represents a connection to the database
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db():
    """
    Dependency for FastAPI endpoints.

    Creates a new database session for each request
    and closes it when the request is done.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
