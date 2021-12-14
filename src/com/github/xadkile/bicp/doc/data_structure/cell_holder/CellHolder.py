from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.TempCell import TempCell
from com.github.xadkile.bicp.doc.data_structure.cell.position.CellPosition import CellPosition


class CellHolder:
    def setCell(self, pos:CellPosition, cell: Cell):
        pass

    def removeCell(self, pos:CellPosition):
        pass

    def hasCellAt(self, pos:CellPosition):
        pass

    def getCell(self, pos:CellPosition) -> Cell:
        pass

    def isEmpty(self) -> bool:
        pass
