import mistune
from typing import Any, Callable, Dict, List, Optional
from .flashcard_parser import FlashcardParser
from .models import FlashcardMetadata, Flashcard, CellFormat
from .mask_generator import MaskGenerator, RowColumnMaskGenerator, MaskInfo

class TsTableParser(FlashcardParser):
    def __init__(
        self,
        cloze_formatter: Optional[Callable[..., str]] = None,
        mask_generator: Optional[MaskGenerator] = None
    ) -> None:
        """
        Initialize the TsTableParser with an optional cloze formatter and mask generator.
        The cloze_formatter can accept any parameters, but must return a string.
        If no formatter is provided, the default Anki cloze pattern is used.
        If no mask_generator is provided, the default RowColumnMaskGenerator is used.
        """
        if cloze_formatter is None:
            self.cloze_formatter = self.default_cloze_formatter
        else:
            self.cloze_formatter = cloze_formatter

        if mask_generator is None:
            self.mask_generator = RowColumnMaskGenerator()
        else:
            self.mask_generator = mask_generator

    def default_cloze_formatter(self) -> str:
        """
        Default cloze formatter that simply hides the information.
        Example: converts "example" to "[...]".
        """
        return f"[...]"

    def parse(self, markdown_content: str, metadata: FlashcardMetadata) -> List[Flashcard]:
        """
        Parse the markdown table from the provided content, generate multiple flashcards
        by applying cloze deletions (via masks) to each row and each column, and return
        the list of flashcards.
        """
        table = self.parse_markdown_table(markdown_content)
        full_table_string = self.format_table(table)
        masks = self.mask_generator.generate_masks(table)
        flashcards: List[Flashcard] = []
        # For each generated mask, apply cloze formatting to create a flashcard.
        for mask in masks:
            masked_table = self.apply_mask(table, mask, cloze_index=1)
            masked_table_string = self.format_table(masked_table)
            flashcards.append(Flashcard(front=masked_table_string, back=full_table_string, metadata=metadata))
        return flashcards

    def parse_markdown_table(self, content: str) -> List[List[str]]:
        """
        Parse a markdown table into a 2D list of strings.
        Assumes that table rows begin and end with the '|' character.
        Skips separator rows (those containing only dashes and pipes) and empty rows.
        """
        lines = [line.strip() for line in content.splitlines() if line.strip().startswith('|')]
        rows: List[List[str]] = []
        for line in lines:
            # Remove the leading and trailing '|' characters.
            if line.startswith('|'):
                line = line[1:]
            if line.endswith('|'):
                line = line[:-1]
            cells = [cell.strip() for cell in line.split('|')]
            # Skip completely empty rows.
            if not any(cell for cell in cells):
                continue
            # Skip alignment/separator rows (cells consisting only of '-' and ':').
            if all(set(cell) <= set('-:') for cell in cells if cell):
                continue
            rows.append(cells)
        return rows

    def format_table(self, table: List[List[str]]) -> str:
        """
        Format a 2D list of strings as an HTML table.
        The entire table is enclosed in a <tbody>.
        The first row cells receive the 'table_header_top' class,
        the first column cells receive the 'table_header_left' class,
        and all cells receive the 'table_body' class.
        """
        if not table:
            return ""
        
        html_lines = ["<table>", "  <tbody>"]
        
        for i, row in enumerate(table):
            html_lines.append("    <tr>")
            for j, cell in enumerate(row):
                classes = ["table_body"]
                if i == 0:
                    classes.append("table_header_top")
                if j == 0:
                    classes.append("table_header_left")
                class_attr = " ".join(classes)
                html_lines.append(f'      <td class="{class_attr}">{cell}</td>')
            html_lines.append("    </tr>")
        
        html_lines.append("  </tbody>")
        html_lines.append("</table>")
        return "\n".join(html_lines)

    def apply_mask(
        self,
        table: List[List[str]],
        mask: List[List[MaskInfo]],
        cloze_index: int = 1
    ) -> List[List[str]]:
        """
        Apply the given mask to the table.
        The mask is a 2D array of MaskInfo objects.
        For cells marked as CLOZE, apply the cloze_formatter.
        Returns a 2D list of strings with the cloze formatting applied.
        """
        num_rows = len(table)
        num_cols = max(len(row) for row in table) if table else 0
        masked_table: List[List[str]] = []
        for i in range(num_rows):
            row: List[str] = []
            for j in range(num_cols):
                cell_text = table[i][j] if j < len(table[i]) else ""
                if mask[i][j].cell_format == CellFormat.CLOZE:
                    cell_text = self.cloze_formatter()
                row.append(cell_text)
            masked_table.append(row)
        return masked_table
