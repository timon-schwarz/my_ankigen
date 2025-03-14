import genanki
import hashlib
from typing import List, Dict
from models.models import Flashcard


def generate_deck_id(name: str) -> int:
    """
    Generate a unique integer ID based on the provided name.
    """
    return int(hashlib.md5(name.encode("utf-8")).hexdigest()[:8], 16)


def group_flashcards_by_deck(flashcards: List[Flashcard]) -> Dict[str, List[Flashcard]]:
    """
    Group flashcards by their 'deck' property.
    Returns a dictionary mapping deck names to lists of flashcards.
    """
    groups = {}
    for card in flashcards:
        groups.setdefault(card.metadata.deck, []).append(card)
    return groups


def build_anki_package(
    flashcards: List[Flashcard], parent_deck_name: str, output_filename: str
) -> None:
    """
    Build an APKG file containing multiple subdecks using the 'ParentDeck::Subdeck' naming convention.
    The note type for each flashcard is determined on a per-card basis using its `note_type` metadata.

    This function groups flashcards by their deck, then for each flashcard, it looks up its note type
    (e.g. "ts_basic") from the NOTE_TYPE_MAP, instantiates the corresponding note type class, and uses it
    to create the genanki.Note.
    """
    groups = group_flashcards_by_deck(flashcards)
    decks = []

    for subdeck_name, cards in groups.items():
        full_deck_name = f"{parent_deck_name}::{subdeck_name}"
        deck_id = generate_deck_id(full_deck_name)
        deck = genanki.Deck(deck_id, full_deck_name)

        for card in cards:
            # Instantiate the note type class for this card.
            model = card.metadata.note_type.create_model()

            note = genanki.Note(
                guid=card.metadata.id, model=model, fields=[card.front, card.back]
            )
            deck.add_note(note)
        decks.append(deck)

    if not decks:
        raise ValueError("No decks to build from the provided flashcards.")

    # Merge notes from all subdecks into a single package.
    package = genanki.Package(decks[0])
    for deck in decks[1:]:
        package.notes.extend(deck.notes)

    package.write_to_file(output_filename)
