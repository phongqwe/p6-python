from typing import List

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.TempCell import TempCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.column.Column import Column
from bicp_document_structure.column.ColumnImp import ColumnImp
from bicp_document_structure.column.MutableColumnContainer import MutableColumnContainer
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.address.RangeAddressImp import RangeAddressImp


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

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        if self.hasCellAt(address):
            return self.__innerCol.getOrMakeCell(address)
        else:
            return TempCell(self, address)

    def isEmpty(self) -> bool:
        return self.__innerCol.isEmpty()

    @property
    def rangeAddress(self) -> RangeAddressImp:
        return self.__innerCol.rangeAddress

    ### >> CellContainer << ###

    def addCell(self, cell: Cell):
        self.__innerCol.addCell(cell)
        # write this temp col to the holder when a new cell is added
        if not self.__holder.hasColumn(self.__innerCol.index):
            self.__holder.setCol(self.__innerCol)

    def removeCell(self, address: CellAddress):
        self.__innerCol.removeCell(address)
