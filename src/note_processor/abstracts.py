from abc import ABC, abstractmethod
from typing import List, Tuple


class Masker(ABC):
    @abstractmethod
    def mask(
        self,
        tables: List[List[List[str]]],
        mask_row_headers: bool,
        mask_col_headers: bool,
    ) -> Tuple[List[List[List[str]]], List[List[List[str]]]]:
        """Returns a unmasked tables and a masked tables."""
        pass


class Parser(ABC):
    @abstractmethod
    def parse(self, content: str) -> List[List[List[str]]]:
        """Parse markdown content to return a list of tables."""
        pass
