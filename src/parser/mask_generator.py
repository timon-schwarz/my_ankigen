from abc import ABC, abstractmethod
from typing import List
from .models import CellFormat, MaskInfo

class MaskGenerator(ABC):
    @abstractmethod
    def generate_masks(self, table: List[List[str]]) -> List[List[List[MaskInfo]]]:
        """
        Generate a list of masks for the provided table.
        Each mask is a 2D array (matching the table dimensions) of MaskInfo objects.
        """
        pass

class RowColumnMaskGenerator(MaskGenerator):
    def generate_masks(self, table: List[List[str]]) -> List[List[List[MaskInfo]]]:
        masks: List[List[List[MaskInfo]]] = []
        num_rows = len(table)
        num_cols = max(len(row) for row in table) if table else 0

        # Generate mask for each row.
        for r in range(num_rows):
            mask: List[List[MaskInfo]] = []
            for i in range(num_rows):
                row_mask: List[MaskInfo] = []
                for j in range(num_cols):
                    if i == r and j != 0:
                        row_mask.append(MaskInfo(cell_format=CellFormat.CLOZE))
                    else:
                        row_mask.append(MaskInfo(cell_format=CellFormat.NORMAL))
                mask.append(row_mask)
            masks.append(mask)

        # Generate mask for each column.
        for c in range(num_cols):
            mask: List[List[MaskInfo]] = []
            for i in range(num_rows):
                row_mask: List[MaskInfo] = []
                for j in range(num_cols):
                    if j == c and i != 0:
                        row_mask.append(MaskInfo(cell_format=CellFormat.CLOZE))
                    else:
                        row_mask.append(MaskInfo(cell_format=CellFormat.NORMAL))
                mask.append(row_mask)
            masks.append(mask)
        return masks
