"""
Places endpoints.

Handles CRUD operations for places.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.place import Place


router = APIRouter()


@router.get("/places")
async def get_places(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[dict]:
    """
    Get list of all places.

    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        db: Database session (injected by FastAPI)

    Returns:
        List[dict]: List of places as dictionaries
    """

    places = db.query(Place).offset(skip).limit(limit).all()

    return [
        {
            "id": place.id,
            "name": place.name,
            "description": place.description,
            "city": place.city,
            "category": place.category,
        }
        for place in places
    ]


@router.get("/places/{place_id}")
async def get_place(place_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Get single place by ID.

    Args:
        place_id: ID of the place to retrieve
        db: Database session (injected by FastAPI)

    Returns:
        dict: Place details
    """

    place = db.query(Place).filter(Place.id == place_id).first()

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    return {
        "id": place.id,
        "name": place.name,
        "description": place.description,
        "city": place.city,
        "category": place.category,
    }


@router.get("/places/search/")
async def search_places(q: str, db: Session = Depends(get_db)) -> List[dict]:
    """
    Search places by name or city.

    Args:
        q: Search query string
        db: Database session (injected by FastAPI)

    Returns:
        List[dict]: List of matching places
    """

    places = (
        db.query(Place)
        .filter((Place.name.ilike(f"%{q}%")) | (Place.city.ilike(f"%{q}%")))
        .limit(20)
        .all()
    )

    return [
        {
            "id": place.id,
            "name": place.name,
            "description": place.description,
            "city": place.city,
            "category": place.category,
        }
        for place in places
    ]
