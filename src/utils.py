from typing import List
from parser.models import Flashcard

def print_flashcards(flashcards: List[Flashcard]) -> None:
    """
    Print a list of flashcards in a formatted and readable manner.
    
    Each flashcard will display its deck, front content, and back content,
    separated by a divider for clarity.
    """
    for idx, card in enumerate(flashcards, 1):
        print(f"Flashcard {idx}:")
        print(f"Deck: {card.deck}")
        print("Front:")
        print(f"{card.front}")
        print("Back:")
        print(f"{card.back}")
        print("-" * 80)
