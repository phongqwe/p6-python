from abc import ABC
from typing import Any, Callable

from pandas import DataFrame

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.cell_container.UserFriendlyCellContainer import UserFriendlyCellContainer


class Range(UserFriendlyCellContainer, MutableCellContainer, ABC):
    """ a sub container derived from a bigger cell container """

    def _toArray(self, extractValueFunction: Callable[[Cell], Any]):
        firstRow = self.firstCellAddress.rowIndex
        lastRow = self.lastCellAddress.rowIndex

        firstCol = self.firstCellAddress.colIndex
        lastCol = self.lastCellAddress.colIndex
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


    def toCopiableArray(self):
        """:return a 2d array for copy-paste operation"""
        def extractSourceValue(cell: Cell):
            return cell.sourceValue
        return self._toArray(extractSourceValue)

    def toValueArray(self):
        """:return a 2d array of values in cell"""
        def extractCellValue(cell: Cell):
            return cell.value
        return self._toArray(extractCellValue)

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
    def sourceContainer(self) -> MutableCellContainer:
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
            sameSourceContainer = self.sourceContainer == o.sourceContainer
            return sameSourceContainer and sameRangeAddress
        else:
            return False

    @property
    def rootRange(self) -> 'Range':
        raise NotImplementedError()
