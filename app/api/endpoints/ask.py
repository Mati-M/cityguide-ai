"""
Ask endpoint for RAG-based questions.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.services import rag
from config import settings

router = APIRouter()


class AskRequest(BaseModel):
    """
    Request model for /ask endpoint.
    """

    question: str


class AskResponse(BaseModel):
    """
    Response model for /ask endpoint.
    """

    answer: str
    sources: list[str] = []


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest, db: Session = Depends(get_db)
) -> AskResponse:
    """
    Ask a question about cities and places.

    Uses RAG to find relevant places and generate an answer.
    """
    # Walidacja
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Generuj odpowiedź
    answer = rag.generate_rag_response(request.question, db)

    # Znajdź źródła (miejsca użyte do odpowiedzi)
    try:
        similar_places = rag.find_similar_places(request.question, db, limit=3)
        sources = [f"{p.name} ({p.city})" for p in similar_places]
    except:
        sources = []

    return AskResponse(answer=answer, sources=sources)
