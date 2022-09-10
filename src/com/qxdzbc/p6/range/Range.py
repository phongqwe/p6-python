from abc import ABC
from typing import Any, Callable, TYPE_CHECKING

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell_container.MutableCellContainer import MutableCellContainer
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey

if TYPE_CHECKING:
    pass



class Range( MutableCellContainer, ABC):
    """ a sub container derived from a bigger cell container """
    @property
    def maxUsedCol(self) -> int | None:
        raise NotImplementedError()

    @property
    def minUsedCol(self) -> int | None:
        raise NotImplementedError()

    @property
    def maxUsedRow(self) -> int | None:
        raise NotImplementedError()

    @property
    def minUsedRow(self) -> int | None:
        raise NotImplementedError()

    def _toArray(self, usedRange: RangeAddress, extractValueFunction: Callable[[Cell], Any]):
        firstRow = usedRange.firstRowIndex
        lastRow = usedRange.lastRowIndex
        firstCol = usedRange.firstColIndex
        lastCol = usedRange.lastColIndex
        rt = []
        for r in range(firstRow, lastRow + 1):
            rowArray = []
            for c in range(firstCol, lastCol + 1):
                if self.hasCellAtIndex(c, r):
                    cell = self.getCell(CellAddresses.fromColRow(c, r)).rootCell
                    rowArray.append(extractValueFunction(cell))
                else:
                    rowArray.append(None)
            if len(rowArray) != 0:
                rt.append(rowArray)
        return rt

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        """:return the smallest range (inside this range) that contains all the existing cell object in this range"""
        if self.minUsedCol and self.maxUsedCol and self.minUsedRow and self.maxUsedRow:
            return RangeAddresses.fromColRow(
                self.minUsedCol, self.maxUsedCol, self.minUsedRow, self.maxUsedRow
            )
        else:
            return None

    @staticmethod
    def __extractCellValue(cell: Cell):
        return cell.value

    @staticmethod
    def __extractSourceValueOfCell(cell: Cell):
        if cell.formula:
            return cell.formula
        else:
            return cell.value

    def toFullValueArray(self):
        """:return a 2d array containing every cell in this range"""
        return self._toArray(self.rangeAddress, self.__extractCellValue)

    def toFullSourceValueArray(self):
        """
        :return: 2d full array of source value
        """
        return self._toArray(self.rangeAddress, self.__extractSourceValueOfCell)

    def toStrictValueArray(self):
        """
        Note: this contains only contains non-empty cell
        :return a 2d array of values in cell
        """
        urange = self.usedRangeAddress
        if urange:
            return self._toArray(urange, self.__extractCellValue)
        else:
            return []

    def toStrictSourceValueArray(self):
        """
        Note: this contains only contains non-empty cell
        :return a 2d array of values in cell
        """
        urange = self.usedRangeAddress
        if urange:
            return self._toArray(urange, self.__extractSourceValueOfCell)
        else:
            return []

    def toRangeCopy(self):
        from com.qxdzbc.p6.rpc.data_structure.range.RangeCopy import \
            RangeCopy
        copyObj = RangeCopy(
            rangeId = self.id,
            cells = self.cells
        )
        return copyObj

    def copySourceValueDataFrame(self):
        """convert this range into a full data array and copy that data frame into the clipboard"""
        raise NotImplementedError()

    def copyStrictSourceValueDataFrame(self):
        raise NotImplementedError()

    def copyToClipboardAsProto(self) -> Result[None, ErrorReport]:
        """ convert this to RangeCopyProto proto bytes, then copy it to clipboard"""
        raise NotImplementedError()

    @property
    def id(self):
        from com.qxdzbc.p6.rpc import \
            RangeId
        return RangeId(
            rangeAddress = self.rangeAddress,
            workbookKey = self.wbKey,
            worksheetName = self.wsName
        )

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
    def wsName(self)->str:
        raise NotImplementedError()

    @property
    def wbKey(self)->WorkbookKey:
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
            sameWs = self.wsName == o.wsName
            sameWbk = self.wbKey == o.wbKey
            return sameWs and sameRangeAddress and sameWbk
        else:
            return False

    @property
    def rootRange(self) -> 'Range':
        raise NotImplementedError()
