from bicp_document_structure.cell.Cell import Cell


class ColumnJson:
    """json facade for Column
    TODO consider removing this class, it seems it is not used anywhere nor has any future use.
    """

    def __init__(self, colIndex: int, cells: list[Cell]):
        self.colIndex = colIndex

        def convertCell(cell:Cell)->dict:
            return cell.toJson().__dict__

        self.cells = list(map(convertCell,cells))
