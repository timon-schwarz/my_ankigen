import os
import logging
import frontmatter
from pathlib import Path
from typing import List
import dotenv
from models.models import Flashcard, NoteMetadata
from note_processor import processor
from deck_builder import deck_builder

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
        with open(md_file, "r", encoding="utf-8") as f:
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

        parser = note_metadata.get("parser")
        if not isinstance(parser, str):
            logging.warning(
                f"File '{md_file}' must have a 'parser' field of type str. Skipping file."
            )
            continue

        masker = note_metadata.get("masker")
        if not isinstance(masker, str):
            logging.warning(
                f"File '{md_file}' must have a 'masker' field of type str. Skipping file."
            )
            continue

        note_metadata = NoteMetadata(
            id=id, name=name, deck=deck, parser=parser, masker=masker
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
