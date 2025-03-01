from typing import List, Tuple
from note_processor.abstracts import Masker
from note_processor import styler


class TableMaskerHiddenVectors(Masker):
    def mask(
        self, tables: List[List[List[str]]]
    ) -> Tuple[List[List[List[str]]], List[List[List[str]]]]:
        unmasked_tables: List[List[List[str]]] = []
        masked_tables: List[List[List[str]]] = []
        for table in tables:
            num_rows = len(table)
            num_cols = max(len(row) for row in table) if table else 0

            # Generate masked table for each row.
            for masked_row_idx in range(num_rows):
                unmasked_table: List[List[str]] = []
                masked_table: List[List[str]] = []
                for row_idx in range(num_rows):
                    unmasked_row_cells: List[str] = []
                    masked_row_cells: List[str] = []
                    for col_idx in range(num_cols):
                        unmasked_cell = table[row_idx][col_idx]
                        if row_idx == masked_row_idx and col_idx != 0:
                            masked_cell = styler.get_masked(unmasked_cell)
                            unmasked_cell = styler.get_unmasked(unmasked_cell)
                            unmasked_row_cells.append(unmasked_cell)
                            masked_row_cells.append(masked_cell)
                        else:
                            unmasked_row_cells.append(unmasked_cell)
                            masked_row_cells.append(unmasked_cell)
                    unmasked_table.append(unmasked_row_cells)
                    masked_table.append(masked_row_cells)
                unmasked_tables.append(unmasked_table)
                masked_tables.append(masked_table)

            # Generate masked table for each column.
            for masked_col_idx in range(num_cols):
                unmasked_table: List[List[str]] = []
                masked_table: List[List[str]] = []
                for row_idx in range(num_rows):
                    unmasked_row_cells: List[str] = []
                    masked_row_cells: List[str] = []
                    for col_idx in range(num_cols):
                        unmasked_cell = table[row_idx][col_idx]
                        if col_idx == masked_col_idx and row_idx != 0:
                            masked_cell = styler.get_masked(unmasked_cell)
                            unmasked_cell = styler.get_unmasked(unmasked_cell)
                            unmasked_row_cells.append(unmasked_cell)
                            masked_row_cells.append(masked_cell)
                        else:
                            unmasked_row_cells.append(unmasked_cell)
                            masked_row_cells.append(unmasked_cell)
                    unmasked_table.append(unmasked_row_cells)
                    masked_table.append(masked_row_cells)
                unmasked_tables.append(unmasked_table)
                masked_tables.append(masked_table)
        return [unmasked_tables, masked_tables]
