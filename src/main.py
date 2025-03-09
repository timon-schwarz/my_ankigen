import os
import logging
import frontmatter
from pathlib import Path
from typing import List
import dotenv
from models.models import Flashcard, NoteMetadata
from note_processor import processor
from deck_builder import deck_builder
from note_processor.abstracts_factory import get_masker, get_parser

logging.basicConfig(level=logging.DEBUG)


def get_markdown_files(root_folder: str) -> List[str]:
    """Recursively yield paths to markdown files in the given folder."""
    md_files: List[str] = []
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    if not md_files:
        logging.warning(f"No markdown files found in folder: {root_folder}")
    return md_files


def generate_flashcards(flashcards_folder: str) -> List[Flashcard]:
    """Process markdown files in the specified flashcards folder and generate flashcards from their metadata and content."""
    flashcards: List[Flashcard] = []
    for md_file in get_markdown_files(flashcards_folder):
        with open(md_file, "r") as f:
            fmatter = frontmatter.load(f)

        note_metadata = fmatter.metadata
        content: str = fmatter.content

        name = Path(md_file).stem

        id = note_metadata.get("id")
        if not isinstance(id, str):
            logging.warning(
                f"File '{md_file}' must have a 'id' field of type str. Skipping file."
            )
            continue

        deck = note_metadata.get("deck")
        if not isinstance(deck, str):
            logging.warning(
                f"File '{md_file}' must have a 'deck' field of type str. Skipping file."
            )
            continue

        parser_type = note_metadata.get("parser")
        parser = get_parser(parser_type)
        if not parser:
            logging.warning(
                f"Parser '{parser_type}' in file '{md_file}' does not exist. Skipping file."
            )
            continue

        masker_type = note_metadata.get("masker")
        masker = get_masker(masker_type)
        if not masker:
            logging.warning(
                f"Masker '{masker_type}' in file '{md_file}' does not exist. Skipping file."
            )
            continue

        mask_row_headers = note_metadata.get("mask_row_headers")
        if (not isinstance(mask_row_headers, bool)) and mask_row_headers == None:
            logging.warning(
                f"'mask_rows' is specified in file '{md_file}' but '{mask_row_headers}' is not a bool. Skipping file."
            )
            continue

        mask_col_headers = note_metadata.get("mask_col_headers")
        if (not isinstance(mask_col_headers, bool)) and mask_col_headers == None:
            logging.warning(
                f"'mask_cols' is specified in file '{md_file}' but '{mask_col_headers}' is not a bool. Skipping file."
            )
            continue

        shuffle_rows = note_metadata.get("shuffle_rows")
        if (not isinstance(shuffle_rows, bool)) and shuffle_rows == None:
            logging.warning(
                f"'shuffle_rows' is specified in file '{md_file}' but '{shuffle_rows}' is not a bool. Skipping file."
            )
            continue

        shuffle_cols = note_metadata.get("shuffle_cols")
        if (not isinstance(shuffle_cols, bool)) and shuffle_cols == None:
            logging.warning(
                f"'shuffle_cols' is specified in file '{md_file}' but '{shuffle_cols}' is not a bool. Skipping file."
            )
            continue

        if shuffle_cols and shuffle_rows:
            logging.warning(
                f"'shuffle_cols' and 'shuffle_rows' is both true in file '{md_file}', which does not make sense. Skipping file."
            )
            continue

        hints = note_metadata.get("hints")
        if not isinstance(hints, list):
            if isinstance(hints, str):
                hints = [hints]
            else:
                hints = []

        note_metadata = NoteMetadata(
            id=id,
            name=name,
            deck=deck,
            parser=parser,
            masker=masker,
            hints=hints,
            mask_col_header=mask_col_headers,
            mask_row_header=mask_row_headers,
            shuffle_cols=shuffle_cols,
            shuffle_rows=shuffle_rows,
        )
        flashcards = processor.process(content, note_metadata)

    return flashcards


def main():
    dotenv.load_dotenv()
    FLASHCARDS_FOLDER = os.getenv("FLASHCARDS_FOLDER")
    if not FLASHCARDS_FOLDER:
        raise ValueError(
            "FLASHCARDS_FOLDER environment variable not set. Please refer to the README on how to create your .env file"
        )
    cards = generate_flashcards(FLASHCARDS_FOLDER)

    for card in cards:
        logging.debug("\n" + str(card))

    parent_deck_name = "my_ankigen"
    output_file = "my_ankigen.apkg"
    deck_builder.build_anki_package(cards, parent_deck_name, output_file)
    logging.info(f"APKG file generated: {output_file}")


if __name__ == "__main__":
    main()
