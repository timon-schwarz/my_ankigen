import genanki
from pathlib import Path

current_dir = Path(__file__).parent

# Global CSS shared by all note types.
with open(current_dir / "note_type_base.css", "r") as f:
    BASE_CSS = f.read()


class BaseNoteType:
    """
    Base class for Anki note types.
    """

    def __init__(
        self, model_id: int, name: str, fields: list, templates: list, css: str = ""
    ):
        self.model_id = model_id
        self.name = name
        self.fields = fields
        self.templates = templates
        self.css = BASE_CSS + "\n" + css

    def create_model(self) -> genanki.Model:
        return genanki.Model(
            self.model_id,
            self.name,
            fields=self.fields,
            templates=self.templates,
            css=self.css,
        )
