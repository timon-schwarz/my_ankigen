from abc import ABC, abstractmethod
from typing import Any, Dict, List
from .models import Flashcard

class FlashcardParser(ABC):
    @abstractmethod
    def parse(self, content: str, metadata: Dict[str, Any]) -> List[Flashcard]:
        """Parse markdown content and metadata to return a list of Flashcards."""
        pass
