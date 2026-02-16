"""
Seed script for initial database data.

Adds sample places to the database.
"""

from app.db.session import SessionLocal
from app.models.place import Place


def seed_places():
    """
    Add sample places to the database.
    """

    db = SessionLocal()

    places = [
        Place(
            name="Rynek w Opolu",
            description="Glowny rynek w Opolu z zabytkowymi kamienicami i "
            "ratuszem. Latem tętni życiem, pełen kawiarni i restauracji.",
            city="Opole",
            category="attraction",
        ),
        Place(
            name="Most Groszowy",
            description="Most zakochanych w Opolu. Pary wieszają kłódki na poręczach jako symbol miłości. Piękny widok na Młynówkę.",
            city="Opole",
            category="attraction",
        ),
        Place(
            name="Wieża Piastowska",
            description="Najstarsza budowla w Opolu, pozostałość po zamku Piastów. Z góry rozpościera się panorama miasta.",
            city="Opole",
            category="monument",
        ),
        Place(
            name="Wyspa Bolko",
            description="Duży park na wyspie w Opolu. Idealny na spacery, rower, pikniki. Jest zoo i tor saneczkowy.",
            city="Opole",
            category="park",
        ),
        Place(
            name="Kawiarnia Czekolada",
            description="Przytulna kawiarnia w centrum Opola. Słynie z gorącej czekolady i domowych ciast.",
            city="Opole",
            category="cafe",
        ),
    ]

    db.add_all(places)

    try:
        db.commit()
        print(f"Added {len(places)} places to database.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_places()
