from abc import ABC
from typing import Optional, Tuple

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.column.Column import Column
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.address.RangeAddress import RangeAddress
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class WorksheetWrapper(Worksheet,ABC):

    def __init__(self, innerWorksheet: Worksheet):
        self._innerSheet: Worksheet = innerWorksheet

    @property
    def name(self) -> str:
        return self._innerSheet.name

    def toJson(self) -> WorksheetJson:
        return self._innerSheet.toJson()

    def cell(self, address: str | CellAddress | Tuple[int, int]) -> Cell:
        return self._innerSheet.cell(address)

    def range(self, rangeAddress: str | RangeAddress | Tuple[CellAddress, CellAddress]) -> Range:
        return self._innerSheet.range(rangeAddress)

    def addCell(self, cell: Cell):
        self._innerSheet.addCell(cell)

    def removeCell(self, address: CellAddress):
        self._innerSheet.removeCell(address)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        return self._innerSheet.getOrMakeCell(address)

    def hasCellAt(self, address: CellAddress) -> bool:
        return self._innerSheet.hasCellAt(address)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        return self._innerSheet.getCell(address)

    def isEmpty(self) -> bool:
        return self._innerSheet.isEmpty()

    def containsAddress(self, address: CellAddress) -> bool:
        return self._innerSheet.containsAddress(address)

    @property
    def cells(self) -> list[Cell]:
        return self._innerSheet.cells

    @property
    def rangeAddress(self) -> RangeAddress:
        return self._innerSheet.rangeAddress

    def setCol(self, col: Column):
        self._innerSheet.setCol(col)

    def removeCol(self, index: int):
        self._innerSheet.removeCol(index)

    def hasColumn(self, colIndex: int) -> bool:
        return self._innerSheet.hasColumn(colIndex)

    def getCol(self, colIndex: int) -> Column:
        return self._innerSheet.getCol(colIndex)

    def toJsonDict(self) -> dict:
        return self._innerSheet.toJsonDict()

    def reportJsonStr(self) -> str:
        return self._innerSheet.reportJsonStr()

    def isSameRangeAddress(self, other):
        return self._innerSheet.isSameRangeAddress(other)

    def reRun(self):
        self._innerSheet.reRun()

    @property
    def innerSheet(self):
        return self._innerSheet