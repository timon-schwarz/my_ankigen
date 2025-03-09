from typing import List
from models.models import Flashcard, NoteMetadata, FlashcardMetadata
from note_processor import styler
from deck_builder.note_type_table import TableNoteType
from deck_builder.note_type_table_shuffled_cols import TableNoteTypeShuffledCols
from deck_builder.note_type_table_shuffled_rows import TableNoteTypeShuffledRows


def build(
    unmasked_tables: List[List[List[str]]],
    masked_tables: List[List[List[str]]],
    note_metadata: NoteMetadata,
) -> List[Flashcard]:
    cards: List[Flashcard] = []
    counter = 0
    for masked_table, unmasked_table in zip(masked_tables, unmasked_tables):
        front = styler.render_table(masked_table)
        front = styler.add_card_header(note_metadata.name, front)
        front = styler.add_hints(note_metadata.hints, front)

        back = styler.render_table(unmasked_table)
        back = styler.add_card_header(note_metadata.name, back)
        back = styler.add_hints(note_metadata.hints, back)

        note_type = TableNoteType()
        if note_metadata.shuffle_cols:
            note_type = TableNoteTypeShuffledCols()
        if note_metadata.shuffle_rows:
            note_type = TableNoteTypeShuffledRows()

        flashcard_metadata = FlashcardMetadata(
            id=note_metadata.id + f"-{counter}",
            deck=note_metadata.deck,
            shuffle_rows=note_metadata.shuffle_rows,
            shuffle_cols=note_metadata.shuffle_cols,
            note_type=note_type,
        )
        cards.append(Flashcard(front=front, back=back, metadata=flashcard_metadata))
        counter += 1
    return cards
