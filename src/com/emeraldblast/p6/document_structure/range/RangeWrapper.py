from abc import ABC
from typing import Optional, Union, Tuple

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class RangeWrapper(Range,ABC):
    def __init__(self, innerRange: Range):
        self._innerRange = innerRange

    @property
    def worksheet(self) -> Worksheet:
        return self.rootRange.worksheet

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        return self.rootRange.deleteCellRs(address)

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        return self.rootRange.deleteRangeRs(rangeAddress)

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

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        return self.rootRange.cell(address)

    def addCell(self, cell: Cell):
        self.rootRange.addCell(cell)

    def deleteCell(self, address: CellAddress):
        self.rootRange.deleteCell(address)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        return self.rootRange.getOrMakeCell(address)

    def hasCellAt(self, address: CellAddress) -> bool:
        return self.rootRange.hasCellAt(address)

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        return self.rootRange.hasCellAtIndex(col,row)

    def containsAddressIndex(self, col: int, row: int) -> bool:
        return self.rootRange.containsAddressIndex(col, row)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        return self.rootRange.getCell(address)

    def isEmpty(self) -> bool:
        return self.rootRange.isEmpty()

    @property
    def cells(self) -> list[Cell]:
        return self.rootRange.cells

    @property
    def rangeAddress(self) -> RangeAddress:
        return self.rootRange.rangeAddress