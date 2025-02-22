from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

class CellFormat(Enum):
    NORMAL = 0
    CLOZE = 1

@dataclass
class FlashcardMetadata:
    name: str
    deck: str
    note_type: str

@dataclass
class Flashcard:
    front: str
    back: str
    metadata: FlashcardMetadata
    def to_string(self) -> str:
        """
        Return a string representation of the flashcard.
        """
        lines = [
            f"Name: {self.metadata.name}",
            f"Deck: {self.metadata.deck}",
            f"Note Type: {self.metadata.note_type}",
            "Front:",
            f"{self.front}",
            "Back:",
            f"{self.back}"
        ]
        return "\n".join(lines)


@dataclass
class MaskInfo:
    cell_format: CellFormat
    meta: Optional[Dict[str, Any]] = None