from typing import List

from bicp_document_structure.cell.Cell import Cell


class ColumnJson(dict):
    """json facade for Column"""

    def __init__(self, colIndex: int, cells: List[Cell]):
        super().__init__()
        self.colIndex = colIndex

        def convertCell(cell:Cell)->dict:
            return cell.toJson().__dict__

        self.cells = list(map(convertCell,cells))
