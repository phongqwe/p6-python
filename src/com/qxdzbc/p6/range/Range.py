import collections
from abc import ABC
from typing import Any, Callable, TYPE_CHECKING, Union, Tuple, Optional

import pandas

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.cell_container.CellContainer import CellContainer
from com.qxdzbc.p6.cell_container.MutableCellContainer import MutableCellContainer
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.range.rpc_data_structure.RangeId import RangeId
from com.qxdzbc.p6.util.CommonError import CommonErrors
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetId import WorksheetId

if TYPE_CHECKING:
    pass


class Range(CellContainer, ABC):
    """ a view derived from a bigger cell container """
    @property
    def wsId(self)->WorksheetId:
        return WorksheetId(self.wbKey,self.wsName)

    def getCell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Optional[Cell]:
        address = CellAddresses.parse(address)
        return self.getCellAtAddress(address)

    def hasCellAt(self, address: CellAddress) -> bool:
        cellOrNone = self.getCellAtAddress(address)
        return cellOrNone is not None

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        return self.hasCellAt(CellAddresses.fromColRow(col,row))

    def assign2dArray(self,data2DArray):
        rs = self.assign2dArrayRs(data2DArray)
        rs.getOrRaise()

    def assign2dArrayRs(self,data2DArray)->Result[None,ErrorReport]:
        raise NotImplementedError()

    def assignDataFrameRs(self,dataFrame)->Result[None,ErrorReport]:
        raise NotImplementedError()

    def assignDataFrame(self,dataFrame):
        rs = self.assignDataFrameRs(dataFrame)
        rs.getOrRaise()
        
    def assignRs(self,dataFrameOr2DArray)->Result[None,ErrorReport]:
        if isinstance(dataFrameOr2DArray,pandas.core.frame.DataFrame):
            return self.assignDataFrameRs(dataFrameOr2DArray)
        elif isinstance(dataFrameOr2DArray,collections.abc.Sequence):
            return self.assign2dArrayRs(dataFrameOr2DArray)
        else:
            return Err(CommonErrors.WrongTypeError.report("can only assign array or DataFrame to a Range"))

    def assign(self,dataFrameOr2DArray):
        rs = self.assignRs(dataFrameOr2DArray)
        rs.getOrRaise()
    @property
    def address(self)->RangeAddress:
        return self.rangeAddress

    @property
    def maxUsedCol(self) -> int | None:
        ur = self.usedRangeAddress
        if ur:
            return ur.lastColIndex
        else:
            return None

    @property
    def minUsedCol(self) -> int | None:
        ur = self.usedRangeAddress
        if ur:
            return ur.firstColIndex
        else:
            return None

    @property
    def maxUsedRow(self) -> int | None:
        ur = self.usedRangeAddress
        if ur:
            return ur.lastRowIndex
        else:
            return None

    @property
    def minUsedRow(self) -> int | None:
        ur = self.usedRangeAddress
        if ur:
            return ur.firstRowIndex
        else:
            return None

    def _toArray(self, usedRange: RangeAddress, extractValueFunction: Callable[[Cell], Any]):
        """convert this range into a 2d array of value"""
        firstRow = usedRange.firstRowIndex
        lastRow = usedRange.lastRowIndex
        firstCol = usedRange.firstColIndex
        lastCol = usedRange.lastColIndex
        rt = []
        for r in range(firstRow, lastRow + 1):
            rowArray = []
            for c in range(firstCol, lastCol + 1):
                if self.hasCellAtIndex(c, r):
                    cell = self.getCellAtAddress(CellAddresses.fromColRow(c, r)).rootCell
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
        from com.qxdzbc.p6.range.rpc_data_structure.RangeCopy import \
            RangeCopy
        copyObj = RangeCopy(
            rangeId = self.id,
            cells = self.cells
        )
        return copyObj

    def copySourceValuesToClipboard(self):
        """convert this range into a full data array and copy that data frame into the clipboard"""
        raise NotImplementedError()

    def copyStrictSourceValuesToClipboard(self):
        raise NotImplementedError()

    def copyToClipboard(self) -> Result[None, ErrorReport]:
        """ convert this to RangeCopyProto proto bytes, then copy it to clipboard"""
        raise NotImplementedError()

    @property
    def id(self):
        return RangeId(
            rangeAddress = self.rangeAddress,
            wbKey = self.wbKey,
            wsName = self.wsName
        )

    @property
    def firstRow(self) -> int:
        return self.rangeAddress.firstRowIndex

    @property
    def lastRow(self) -> int:
        return self.rangeAddress.lastRowIndex

    @property
    def firstCol(self) -> int:
        return self.rangeAddress.firstColIndex

    @property
    def lastCol(self) -> int:
        return self.rangeAddress.lastColIndex

    @property
    def firstCellAddress(self) -> CellAddress:
        return self.rangeAddress.topLeft

    @property
    def lastCellAddress(self) -> CellAddress:
        return self.rangeAddress.botRight

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
