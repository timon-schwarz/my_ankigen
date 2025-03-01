from typing import List
from models.models import Flashcard, NoteMetadata
from note_processor import abstracts_factory
from note_processor import builder


def process(content: str, note_metadata: NoteMetadata) -> List[Flashcard]:
    """Process content to generate one or more Flashcards"""
    parser = abstracts_factory.get_parser(note_metadata.parser)
    masker = abstracts_factory.get_masker(note_metadata.masker)

    tables = parser.parse(content)
    unmasked_tables, masked_tables = masker.mask(tables)
    cards = builder.build(unmasked_tables, masked_tables, note_metadata)
    return cards
