import os
import logging
import frontmatter
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from parser.get_parser import get_parser
from parser.models import Flashcard, FlashcardMetadata
from deck_builder.deck_builder import build_anki_package

logging.basicConfig(level=logging.DEBUG)


def get_markdown_files(root_folder: str) -> List[str]:
    """Recursively yield paths to markdown files in the given folder."""
    md_files: List[str] = []
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    if not md_files:
        logging.warning(f"No markdown files found in folder: {root_folder}")
    return md_files

def process_flashcards(flashcards_folder: str) -> List[Flashcard]:
    """Process markdown files in the specified flashcards folder and generate flashcards from their metadata and content."""
    flashcards: List[Flashcard] = []
    for md_file in get_markdown_files(flashcards_folder):
        with open(md_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        metadata = post.metadata
        content: str = post.content

        name = Path(md_file).stem

        unique_id = metadata.get('unique_id')
        if not isinstance(unique_id, str):
            logging.warning(f"File '{md_file}' must have a 'unique_id' field of type str. Skipping file.")
            continue

        deck = metadata.get('deck')
        if not isinstance(deck, str):
            logging.warning(f"File '{md_file}' must have a 'deck' field of type str. Skipping file.")
            continue

        note_type = metadata.get('note_type')
        if not isinstance(note_type, str):
            logging.warning(f"File '{md_file}' must have a 'note_type' field of type str. Skipping file.")
            continue

        flashcard_metadata = FlashcardMetadata(unique_id=unique_id, name=name, deck=deck, note_type=note_type)

        parser = get_parser(note_type)
        if parser is None:
            logging.warning(f"Unknown note type '{note_type}' in file {md_file}. Skipping file.")
            continue

        flashcards = parser.parse(content, flashcard_metadata)

    return flashcards


if __name__ == '__main__':
    load_dotenv()
    FLASHCARDS_FOLDER = os.getenv("FLASHCARDS_FOLDER")
    if not FLASHCARDS_FOLDER :
        raise ValueError("FLASHCARDS_FOLDER environment variable not set. Please refer to the README on how to create your .env file")
    cards = process_flashcards(FLASHCARDS_FOLDER)

    for card in cards:
        logging.debug("\n" + card.to_string())

    parent_deck_name = "my_ankigen"
    output_file = "my_ankigen.apkg"
    build_anki_package(cards, parent_deck_name, output_file)
    logging.info(f"APKG file generated: {output_file}")
