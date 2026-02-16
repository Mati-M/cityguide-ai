"""
Place model for the database.

Represents a location in a city that users can ask about.
"""

from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base


class Place(Base):
    """
    Place model.

    Attributes:
        id: Unique identifier
        name: Name of the place (e.g., "Rynek w Opolu")
        description: Detailed description of the place
        city: City name (e.g., "Opole", "Wrocław")
        category: Type of place (e.g., "monument", "cafe", "park")
    """

    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    embedding = Column(String, nullable=True)

    def __repr__(self) -> str:
        """
        String representation of the Place object.

        Returns:
            str: Readable representation
        """
        return f"<Place(name='{self.name}', city='{self.city}')>"
