"""
Generate embeddings for all places.

This script reads all places from the database,
generates embeddings using OpenAI API,
and saves them back to the database.
"""

import openai
from app.db.session import SessionLocal
from app.models.place import Place
from config import settings

# Inicjalizacja OpenAI
openai.api_key = settings.openai_api_key


def generate_embedding(text: str) -> list:
    """
    Generate embedding for a given text using OpenAI API.

    Args:
        text: Input text to generate embedding for

    Returns:
        list: Embedding vector as list of floats
    """
    response = openai.embeddings.create(
        model="text-embedding-3-small", input=text, encoding_format="float"
    )
    return response.data[0].embedding


def generate_all_embeddings():
    """
    Generate embeddings for all places that don't have them yet.
    """
    db = SessionLocal()

    # Pobierz wszystkie miejsca bez embeddingu
    places = db.query(Place).filter(Place.embedding.is_(None)).all()

    print(f"Found {len(places)} places without embeddings.")

    for i, place in enumerate(places, 1):
        print(f"Generating embedding for {place.name} ({i}/{len(places)})...")

        # Połącz nazwę, kategorię i opis w jeden tekst
        text_to_embed = f"{place.name}. {place.category}. {place.description}"

        try:
            # Generuj embedding
            embedding = generate_embedding(text_to_embed)

            # Zapisz w bazie (na razie jako string)
            place.embedding = str(embedding)
            db.commit()

            print(f"Done")

        except Exception as e:
            print(f"Error: {e}")
            db.rollback()

    db.close()
    print("Finished generating embeddings.")


if __name__ == "__main__":
    # Sprawdź czy klucz API nie jest testowy
    if settings.openai_api_key == "sk-test":
        print("WARNING: Using test API key. Set real OPENAI_API_KEY in .env")
    else:
        generate_all_embeddings()
