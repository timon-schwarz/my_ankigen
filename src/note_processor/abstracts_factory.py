from note_processor.abstracts import Parser, Masker
from note_processor.table_parser import TableParser
from note_processor.table_masker_hidden_vectors import TableMaskerHiddenVectors


def get_masker(masker: str) -> Masker:
    """Return an instance of the appropriate masker based on the provided string."""
    if masker == "vectors":
        return TableMaskerHiddenVectors()
    return None


def get_parser(parser: str) -> Parser:
    """Return an instance of the appropriate parser based on the provided string."""
    if parser == "table":
        return TableParser()
    return None
