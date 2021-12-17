from typing import List

from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.TempCell import TempCell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress
from com.github.xadkile.bicp.doc.data_structure.column.Column import Column
from com.github.xadkile.bicp.doc.data_structure.column.ColumnContainer import MutableColumnContainer
from com.github.xadkile.bicp.doc.data_structure.column.ColumnImp import ColumnImp
from com.github.xadkile.bicp.doc.data_structure.range.Range import Range
from com.github.xadkile.bicp.doc.data_structure.range.RangeAddress import RangeAddress


class TempColumn(Column):
    def __init__(self, colIndex: int, holder: MutableColumnContainer):
        self.__holder = holder
        if holder.hasColumn(colIndex):
            self.__innerCol = holder.getCol(colIndex)
        else:
            self.__innerCol = ColumnImp(colIndex, {})

    ### >> Column << ##

    def range(self, firstRow: int, lastRow: int) -> Range:
        return self.__innerCol.range(firstRow, lastRow)

    @property
    def index(self) -> int:
        return self.__innerCol.index

    ### >> Range << ###

    @property
    def firstCellAddress(self) -> CellAddress:
        return self.__innerCol.firstCellAddress

    @property
    def lastCellAddress(self) -> CellAddress:
        return self.__innerCol.lastCellAddress

    def containsAddress(self, address: CellAddress) -> bool:
        return self.__innerCol.containsAddress(address)

    @property
    def cells(self) -> List[Cell]:
        return self.__innerCol.cells

    ### >> CellContainer << ###

    def hasCellAt(self, address: CellAddress) -> bool:
        return self.__innerCol.hasCellAt(address)

    def getCell(self, address: CellAddress) -> Cell:
        if self.hasCellAt(address):
            return self.__innerCol.getCell(address)
        else:
            return TempCell(self, address)

    def isEmpty(self) -> bool:
        return self.__innerCol.isEmpty()

    @property
    def rangeAddress(self) -> RangeAddress:
        return self.__innerCol.rangeAddress

    ### >> CellContainer << ###

    def addCell(self, cell: Cell):
        self.__innerCol.addCell(cell)
        # write this temp col to the holder when a new cell is added
        if not self.__holder.hasColumn(self.__innerCol.index):
            self.__holder.setCol(self.__innerCol.index, self.__innerCol)

    def removeCell(self, address: CellAddress):
        self.__innerCol.removeCell(address)
