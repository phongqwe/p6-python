from typing import List

from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellIndex import CellIndex
from com.github.xadkile.bicp.doc.data_structure.column.Column import Column
from com.github.xadkile.bicp.doc.data_structure.column.TempColumn import TempColumn
from com.github.xadkile.bicp.doc.data_structure.range.RangeAddress import RangeAddress
from com.github.xadkile.bicp.doc.data_structure.sheet.Worksheet import Worksheet
from com.github.xadkile.bicp.doc.data_structure.sheet.WorksheetConst import WorksheetConst


class WorksheetImp(Worksheet):
    def __init__(self, colDict=None, name=""):
        if colDict is None:
            colDict = {}
        self.__colDict = colDict
        self.__name = name

    ### >> Worksheet << ###
    @property
    def name(self) -> str:
        return self.__name

    ### >> CellContainer << ###

    def hasCellAt(self, address: CellAddress) -> bool:
        if self.hasColumn(address.colIndex):
            return self.getCol(address.colIndex).hasCellAt(address)
        else:
            return False

    def getCell(self, address: CellAddress) -> Cell:
        col = self.getCol(address.colIndex)
        rt = col.getCell(address)
        return rt

    def isEmpty(self) -> bool:
        return not bool(self.__colDict)

    def containsAddress(self, address: CellAddress) -> bool:
        if self.hasColumn(address.colIndex):
            return self.getCol(address.colIndex).containsAddress(address)
        else:
            return False

    @property
    def cells(self) -> List[Cell]:
        rt = []
        for k, v in (self.__colDict.items()):
            rt.extend(v.cells)
        return rt

    @property
    def rangeAddress(self) -> RangeAddress:
        return RangeAddress(
            CellIndex(1, 1),
            CellIndex(WorksheetConst.colLimit, WorksheetConst.rowLimit)
        )

    ### >> MutableCellContainer << ###

    def addCell(self, cell: Cell):
        self.getCol(cell.col).addCell(cell)

    def removeCell(self, address: CellAddress):
        col = self.getCol(address.colIndex)
        col.removeCell(address)
        if col.isEmpty():
            self.removeCol(col.index)

    ### >> MutableColumnContainer << ###

    def setCol(self, col: Column):
        if isinstance(col, Column):
            self.__colDict[col.index] = col
        else:
            raise ValueError("input col is not of type Column")

    def removeCol(self, index: int):
        del self.__colDict[index]

    ### >> ColumnContainer << ###

    def hasColumn(self, colIndex: int) -> bool:
        return colIndex in self.__colDict.keys()

    def getCol(self, colIndex: int) -> Column:
        if self.hasColumn(colIndex):
            return self.__colDict[colIndex]
        else:
            return TempColumn(colIndex, self)
