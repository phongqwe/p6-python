from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.position.CellPosition import CellPosition


class CellContainer:
    def addCell(self, cell: Cell):
        """add a cell to this holder"""
        pass

    def removeCell(self, pos:CellPosition):
        """remove the cell at the specified position"""
        pass

    def hasCellAt(self, pos:CellPosition)->bool:
        """:return true if this holder has a cell at the specified position"""
        pass

    def getCell(self, pos:CellPosition) -> Cell:
        """:return the cell at the position"""
        pass

    def isEmpty(self) -> bool:
        """:return true if this holder is empty"""
        pass
