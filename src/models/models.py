from dataclasses import dataclass, field
from typing import List
from deck_builder.note_type_base import BaseNoteType
from note_processor.abstracts import Masker, Parser


@dataclass(slots=True, kw_only=True)
class NoteMetadata:
    id: str
    name: str
    deck: str
    parser: Parser
    masker: Masker
    mask_row_header: bool
    mask_col_header: bool
    shuffle_rows: bool
    shuffle_cols: bool
    hints: List[str] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class FlashcardMetadata:
    id: str
    deck: str
    shuffle_rows: bool
    shuffle_cols: bool
    note_type: BaseNoteType


@dataclass(slots=True, kw_only=True)
class Flashcard:
    front: str
    back: str
    metadata: FlashcardMetadata

    def __repr__(self) -> str:
        """
        Return a string representation of the flashcard for debugging.
        """
        lines = [
            self.metadata.__repr__(),
            "Front:",
            f"{self.front}",
            "Back:",
            f"{self.back}" "-" * 100,
        ]
        return "\n".join(lines)

    def __str__(self) -> str:
        """
        Return a simple string representation of the flashcard.
        """
        lines = [
            "ID: " + str(self.metadata.id),
            "Deck: " + str(self.metadata.deck),
            "Type: " + str(self.metadata.note_type),
            "-" * 100,
        ]
        return "\n".join(lines)
