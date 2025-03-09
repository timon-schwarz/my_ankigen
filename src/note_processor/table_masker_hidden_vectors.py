from typing import List, Tuple
from note_processor.abstracts import Masker
from note_processor import styler


class TableMaskerHiddenVectors(Masker):
    def mask(
        self,
        tables: List[List[List[str]]],
        mask_row_headers: bool,
        mask_col_headers: bool,
    ) -> Tuple[List[List[List[str]]], List[List[List[str]]]]:
        unmasked_tables: List[List[List[str]]] = []
        masked_tables: List[List[List[str]]] = []
        for table in tables:
            num_rows = len(table)
            num_cols = max(len(row) for row in table) if table else 0

            # Generate masked table for each row.
            for masked_row_idx in range(num_rows):
                if masked_row_idx == 0 and not mask_col_headers:
                    continue
                unmasked_table: List[List[str]] = []
                masked_table: List[List[str]] = []
                for row_idx in range(num_rows):
                    unmasked_row_cells: List[str] = []
                    masked_row_cells: List[str] = []
                    for col_idx in range(num_cols):
                        cell_content = table[row_idx][col_idx]
                        if row_idx == masked_row_idx and col_idx != 0:
                            unmasked = styler.get_unmasked(cell_content)
                            masked = styler.get_masked(cell_content)
                            unmasked_row_cells.append(unmasked)
                            masked_row_cells.append(masked)
                        else:
                            unmasked_row_cells.append(cell_content)
                            masked_row_cells.append(cell_content)
                    unmasked_table.append(unmasked_row_cells)
                    masked_table.append(masked_row_cells)
                unmasked_tables.append(unmasked_table)
                masked_tables.append(masked_table)

            # Generate masked table for each column.
            for masked_col_idx in range(num_cols):
                if masked_col_idx == 0 and not mask_row_headers:
                    continue
                unmasked_table: List[List[str]] = []
                masked_table: List[List[str]] = []
                for row_idx in range(num_rows):
                    unmasked_row_cells: List[str] = []
                    masked_row_cells: List[str] = []
                    for col_idx in range(num_cols):
                        cell_content = table[row_idx][col_idx]
                        if col_idx == masked_col_idx and row_idx != 0:
                            unmasked = styler.get_unmasked(cell_content)
                            masked = styler.get_masked(cell_content)
                            unmasked_row_cells.append(unmasked)
                            masked_row_cells.append(masked)
                        else:
                            unmasked_row_cells.append(cell_content)
                            masked_row_cells.append(cell_content)
                    unmasked_table.append(unmasked_row_cells)
                    masked_table.append(masked_row_cells)
                unmasked_tables.append(unmasked_table)
                masked_tables.append(masked_table)
        return [unmasked_tables, masked_tables]
