"""
RAG (Retrieval-Augmented Generation) service.

Handles semantic search and LLM interactions.
"""

import openai
from sqlalchemy.orm import Session
from typing import List

from app.models.place import Place
from config import settings

# Inicjalizacja OpenAI
openai.api_key = settings.openai_api_key


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a given text using OpenAI API.

    Args:
        text: Input text to generate embedding for

    Returns:
        List[float]: Embedding vector
    """
    response = openai.embeddings.create(
        model="text-embedding-3-small", input=text, encoding_format="float"
    )
    return response.data[0].embedding


def find_similar_places(
    query: str, db: Session, limit: int = 5
) -> List[Place]:
    """
    Find places similar to the query using vector similarity.

    Args:
        query: User's question
        db: Database session
        limit: Maximum number of places to return

    Returns:
        List[Place]: Most similar places
    """
    # Jeśli nie ma embeddingów, zwróć puste miejsce
    first_place = db.query(Place).first()
    if first_place is None or first_place.embedding is None:
        print("No embeddings found. Please run generate_embeddings.py first.")
        return []

    # 1. Generate embedding for the query
    query_embedding = generate_embedding(query)

    # 2. Search for similar places using cosine distance
    #    <=> is the cosine distance operator in pgvector
    similar_places = (
        db.query(Place)
        .order_by(Place.embedding.cosine_distance(query_embedding))
        .limit(limit)
        .all()
    )

    return similar_places


def generate_rag_response(query: str, db: Session) -> str:
    """
    Generate RAG response for user query.

    Args:
        query: User's question
        db: Database session

    Returns:
        str: LLM response based on retrieved context
    """
    # Sprawdź czy mamy klucz API
    if settings.openai_api_key == "sk-test":
        return (
            "OpenAI API key not configured. Please set OPENAI_API_KEY in .env"
        )

    # 1. Find similar places
    similar_places = find_similar_places(query, db)

    if not similar_places:
        return "Przepraszam, nie mam wystarczających informacji na ten temat."

    # 2. Build context from similar places
    context = "\n\n".join(
        [
            f"Miejsce: {p.name}\n"
            f"Kategoria: {p.category}\n"
            f"Opis: {p.description}\n"
            f"Miasto: {p.city}"
            for p in similar_places
        ]
    )

    # 3. Build prompt
    system_prompt = """Jesteś pomocnym przewodnikiem turystycznym.
Odpowiadasz na pytania dotyczące miast i miejsc na podstawie dostarczonego kontekstu.
Jeśli nie znasz odpowiedzi lub nie ma jej w kontekście, przyznaj się do tego.
Odpowiadaj w języku polskim, w sposób przyjazny i pomocny.
"""

    user_prompt = f"""
KONTEKST (informacje o miejscach):
{context}

PYTANIE UŻYTKOWNIKA:
{query}

ODPOWIEDŹ (na podstawie kontekstu):
"""

    # 4. Call OpenAI
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return "Przepraszam, wystąpił problem z generowaniem odpowiedzi."
