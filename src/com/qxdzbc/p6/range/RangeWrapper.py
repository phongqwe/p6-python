from abc import ABC
from typing import Optional, Union, Tuple

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


class RangeWrapper(Range):

    def assign2dArrayRs(self, data2DArray) -> Result[None, ErrorReport]:
        return self.rootRange.assign2dArrayRs(data2DArray)

    def assignDataFrameRs(self, dataFrame) -> Result[None, ErrorReport]:
        return self.rootRange.assignDataFrameRs(dataFrame)

    def __init__(self, innerRange: Range):
        self._innerRange = innerRange



    def copySourceValuesToClipboard(self):
        self.rootRange.copySourceValuesToClipboard()

    def copyStrictSourceValuesToClipboard(self):
        self.rootRange.copyStrictSourceValuesToClipboard()

    def copyToClipboard(self) -> Result[None, ErrorReport]:
        return self.rootRange.copyToClipboard()

    @property
    def wsName(self) -> str:
        return self.rootRange.wsName

    @property
    def wbKey(self) -> WorkbookKey:
        return self.rootRange.wbKey

    @property
    def size(self) -> int:
        return self.rootRange.size

    @property
    def rootRange(self)->'Range':
        return self._innerRange.rootRange
    
    @property
    def firstCellAddress(self) -> CellAddress:
        return self.rootRange.firstCellAddress

    @property
    def lastCellAddress(self) -> CellAddress:
        return self.rootRange.lastCellAddress

    def getCell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        return self.rootRange.getCell(address)

    def hasCellAt(self, address: CellAddress) -> bool:
        return self.rootRange.hasCellAt(address)

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        return self.rootRange.hasCellAtIndex(col,row)

    def containsAddressIndex(self, col: int, row: int) -> bool:
        return self.rootRange.containsAddressIndex(col, row)

    def getCellAtAddress(self, address: CellAddress) -> Optional[Cell]:
        return self.rootRange.getCellAtAddress(address)

    def isEmpty(self) -> bool:
        return self.rootRange.isEmpty()

    @property
    def cells(self) -> list[Cell]:
        return self.rootRange.cells

    @property
    def rangeAddress(self) -> RangeAddress:
        return self.rootRange.rangeAddress