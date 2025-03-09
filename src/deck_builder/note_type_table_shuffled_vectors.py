from pathlib import Path
from deck_builder.note_type_base import BaseNoteType


current_dir = Path(__file__).parent

# Additional CSS specific to this note type.
ADDITIONAL_CSS = ""
with open(current_dir / "note_type_table.css", "r") as f:
    ADDITIONAL_CSS = f.read()

# JavaScript to shuffle the rows and columns in the question
SHUFFLE_JS_QUESTION = ""
with open(current_dir / "shuffle_vectors_question.js", "r") as f:
    SHUFFLE_JS_QUESTION = f.read()

# JavaScript to shuffle the rows and columns in the answer
SHUFFLE_JS_ANSWER = ""
with open(current_dir / "shuffle_vectors_answer.js", "r") as f:
    SHUFFLE_JS_ANSWER = f.read()


class TableNoteTypeShuffledVectors(BaseNoteType):
    """
    A basic note type for ts_table flashcards.

    - Front: rendered as HTML.
    - Back: rendered as HTML.
    """

    def __init__(self):
        fields = [{"name": "Front"}, {"name": "Back"}]
        templates = [
            {
                "name": "ts_table",
                "qfmt": "\n".join(
                    [
                        "<script>",
                        SHUFFLE_JS_QUESTION,
                        "</script>",
                        '<div class="card">',
                        '<div class="card-content">',
                        "",
                        "{{Front}}",
                        "",
                        "</div>",
                        "</div>",
                    ]
                ),
                "afmt": "\n".join(
                    [
                        "<script>",
                        SHUFFLE_JS_ANSWER,
                        "</script>",
                        '<div class="card">',
                        '<div class="card-content">',
                        "",
                        "{{Back}}",
                        "",
                        "</div>",
                        "</div>",
                    ]
                ),
            }
        ]
        # Ensure the model ID is unique.
        super().__init__(
            model_id=1741545257,
            name="ts_table_shuffled_vectors",
            fields=fields,
            templates=templates,
            css=ADDITIONAL_CSS,
        )
