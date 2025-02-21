from parser.models import Flashcard, CellFormat
from parser.flashcard_parser import FlashcardParser
from parser.ts_table_parser import TsTableParser

def get_parser(note_type: str):
    """
    Return an instance of the appropriate parser based on the provided note_type.
    Currently supports:
      - "ts_table": Returns a TsTableParser instance.
    If the note_type is unrecognized, returns None.
    """
    if note_type == "ts_table":
        return TsTableParser()
    return None
