from typing import List
from models.models import Flashcard, NoteMetadata, FlashcardMetadata
from note_processor import styler
from deck_builder.note_types import TableNoteType


def build(
    unmasked_tables: List[List[List[str]]],
    masked_tables: List[List[List[str]]],
    note_metadata: NoteMetadata,
) -> List[Flashcard]:
    cards: List[Flashcard] = []
    counter = 0
    for masked_table, unmasked_table in zip(masked_tables, unmasked_tables):
        unmasked_string = styler.render_table(unmasked_table)
        masked_string = styler.render_table(masked_table)
        front = styler.add_card_header(note_metadata.name, masked_string)
        back = styler.add_card_header(note_metadata.name, unmasked_string)
        # TODO: Differentiate note types
        flashcard_metadata = FlashcardMetadata(
            id=note_metadata.id + f"-{counter}",
            deck=note_metadata.deck,
            note_type=TableNoteType,
        )
        cards.append(Flashcard(front=front, back=back, metadata=flashcard_metadata))
        counter += 1
    return cards
