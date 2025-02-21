from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

class CellFormat(Enum):
    NORMAL = 0
    CLOZE = 1

@dataclass
class FlashcardMetadata:
    deck: str

@dataclass
class Flashcard:
    front: str
    back: str
    metadata: FlashcardMetadata


@dataclass
class MaskInfo:
    cell_format: CellFormat
    meta: Optional[Dict[str, Any]] = None