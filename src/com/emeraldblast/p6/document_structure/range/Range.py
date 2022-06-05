from abc import ABC
from typing import Any, Callable, TYPE_CHECKING

from pandas import DataFrame

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.cell_container.UserFriendlyCellContainer import UserFriendlyCellContainer
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses

if TYPE_CHECKING:
    from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class Range(UserFriendlyCellContainer, MutableCellContainer, ABC):
    """ a sub container derived from a bigger cell container """

    def _toArray(self, usedRange:RangeAddress ,extractValueFunction: Callable[[Cell], Any]):
        firstRow = usedRange.firstRowIndex
        lastRow = usedRange.lastRowIndex
        firstCol = usedRange.firstColIndex
        lastCol = usedRange.lastColIndex
        rt = []
        for r in range(firstRow, lastRow + 1):
            rowArray = []
            for c in range(firstCol, lastCol + 1):
                if self.hasCellAtIndex(c, r):
                    rowArray.append(extractValueFunction(self.getCell(CellAddresses.fromColRow(c, r)).rootCell))
                else:
                    rowArray.append(None)
            if len(rowArray) != 0:
                rt.append(rowArray)
        return rt

    @property
    def usedRange(self) -> RangeAddress|None:
        """:return the smallest range (inside this range) that contains all the existing cell object in this range"""
        if self.isEmpty():
            return None
        else:
            cells = self.cells
            firstCell = cells[0]
            maxRow = minRow = firstCell.row
            maxCol = minCol = firstCell.col
            for cell in self.cells:
                if cell.row > maxRow:
                    maxRow = cell.row
                if cell.row < minRow:
                    minRow = cell.row
                if cell.col > maxCol:
                    maxCol = cell.col
                if cell.col < minCol:
                    minCol = cell.col
            return RangeAddresses.from2Cells(
                firstCell = CellAddresses.fromColRow(minCol,minRow),
                secondCell = CellAddresses.fromColRow(maxCol,maxRow)
            )

    def toCopiableArray(self):
        """:return a 2d array for copy-paste operation"""
        def extractSourceValue(cell: Cell):
            return cell.sourceValue
        return self._toArray(self.usedRange,extractSourceValue)


    def toValueArray(self):
        """:return a 2d array of values in cell"""
        # todo this is slow as hell, improve it

        def extractCellValue(cell: Cell):
            return cell.value

        return self._toArray(self.rangeAddress,extractCellValue)

    def copyToClipboard(self):
        """convert this range into a data frame and copy that data frame into the clipboard"""
        df = DataFrame.from_records(self.toCopiableArray())
        df.to_clipboard(excel = True, index = False, header = None)

    @property
    def firstRow(self) -> int:
        return self.firstCellAddress.rowIndex

    @property
    def lastRow(self) -> int:
        return self.lastCellAddress.rowIndex

    @property
    def firstCol(self) -> int:
        return self.firstCellAddress.colIndex

    @property
    def lastCol(self) -> int:
        return self.lastCellAddress.colIndex

    @property
    def firstCellAddress(self) -> CellAddress:
        raise NotImplementedError()

    @property
    def lastCellAddress(self) -> CellAddress:
        raise NotImplementedError()

    @property
    def worksheet(self) -> 'Worksheet':
        raise NotImplementedError()

    def containsAddress(self, address: CellAddress) -> bool:
        return self.containsAddressIndex(address.colIndex, address.rowIndex)

    def containsAddressIndex(self, col: int, row: int) -> bool:
        rowIsInRange = self.firstCellAddress.rowIndex <= row <= self.lastCellAddress.rowIndex
        colIsInRange = self.firstCellAddress.colIndex <= col <= self.lastCellAddress.colIndex
        return rowIsInRange and colIsInRange

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Range):
            sameRangeAddress = self.isSameRangeAddress(o)
            sameSourceContainer = self.worksheet == o.worksheet
            return sameSourceContainer and sameRangeAddress
        else:
            return False

    @property
    def rootRange(self) -> 'Range':
        raise NotImplementedError()
