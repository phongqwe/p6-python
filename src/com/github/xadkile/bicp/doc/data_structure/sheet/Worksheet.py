from typing import List

from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress
from com.github.xadkile.bicp.doc.data_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.github.xadkile.bicp.doc.data_structure.column.ColumnContainer import MutableColumnContainer
from com.github.xadkile.bicp.doc.data_structure.range.RangeAddress import RangeAddress


class Worksheet(MutableCellContainer, MutableColumnContainer):

    def __init__(self, colDict=None):
        if colDict is None:
            colDict = {}
        self.__colDict = colDict
    ### >> CellContainer << ###
    def hasCellAt(self, address: CellAddress) -> bool:
        if self.hasColumn(address.colIndex):
            return self.getCol(address.colIndex).hasCellAt(address)
        else:
            return False

    def getCell(self, address: CellAddress) -> Cell:
        return self.getCol(address.colIndex).getCell(address)

    def isEmpty(self) -> bool:
        return not bool(self.__colDict)

    def containsAddress(self, address: CellAddress) -> bool:
        if self.hasColumn(address.colIndex):
            return self.getCol(address.colIndex).containsAddress(address)
        else:
            return False

    @property
    def cells(self) -> List[Cell]:
        return super().cells()

    @property
    def rangeAddress(self) -> RangeAddress:
        return super().rangeAddress()

    ### >> MutableCellContainer << ###
    def addCell(self, cell: Cell):
        self.getCol(cell.col).addCell(cell)

    def removeCell(self, address: CellAddress):
        self.getCol(address.colIndex).removeCell(address)
