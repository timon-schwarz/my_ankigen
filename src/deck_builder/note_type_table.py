from pathlib import Path
from deck_builder.note_type_base import BaseNoteType

current_dir = Path(__file__).parent

# Additional CSS specific to this note type.
ADDITIONAL_CSS = ""
with open(current_dir / "note_type_table.css", "r") as f:
    ADDITIONAL_CSS = f.read()


class TableNoteType(BaseNoteType):
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
            model_id=1607392319,
            name="ts_table",
            fields=fields,
            templates=templates,
            css=ADDITIONAL_CSS,
        )
