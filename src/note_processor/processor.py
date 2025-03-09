from typing import List
from models.models import Flashcard, NoteMetadata
from note_processor import builder


def process(content: str, note_metadata: NoteMetadata) -> List[Flashcard]:
    """Process content to generate one or more Flashcards"""
    tables = note_metadata.parser.parse(content)
    unmasked_tables, masked_tables = note_metadata.masker.mask(
        tables, note_metadata.mask_row_header, note_metadata.mask_col_header
    )
    cards = builder.build(unmasked_tables, masked_tables, note_metadata)
    return cards
