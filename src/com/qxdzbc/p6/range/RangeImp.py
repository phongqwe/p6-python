import copy
from typing import Optional, Union, Tuple

from com.qxdzbc.p6.cell import WriteBackCell

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.RangeErrors import RangeErrors
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.range.address.RangeAddressImp import RangeAddressImp
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.util.AddressParser import AddressParser
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


class RangeImp(Range):
    """ an immutable sub container of a bigger cell container"""

    def __init__(self, firstCellAddress: CellAddress, lastCellAddress: CellAddress,
                 sourceContainer: Worksheet):

        rangeIsValid = sourceContainer.containsAddress(firstCellAddress) and sourceContainer.containsAddress(
            lastCellAddress)
        rAddress = RangeAddressImp(firstCellAddress, lastCellAddress)
        if rangeIsValid:
            self.__rangeAddress = rAddress
            self.__firstCell = firstCellAddress
            self.__lastCell = lastCellAddress
            self.__worksheet = sourceContainer

            self._minUsedCol = None
            self._maxUsedCol = None
            self._minUsedRow = None
            self._maxUsedRow = None

            self._updateExtremeColRow()

        else:
            raise ValueError("container {sc} does not contain range {r}".format(
                sc = str(sourceContainer.rangeAddress), r = str(rAddress)
            ))

    @property
    def maxUsedCol(self) -> int | None:
        return self._maxUsedCol

    @property
    def minUsedCol(self) -> int | None:
        return self._minUsedCol

    @property
    def maxUsedRow(self) -> int | None:
        return self._maxUsedRow

    @property
    def minUsedRow(self) -> int | None:
        return self._minUsedRow

    def _updateExtremeColRow(self):
        needToUpdateMaxCol = True
        needToUpdateMinCol = True
        needToUpdateMaxRow = True
        needToUpdateMinRow = True
        if not self.isEmpty():
            if self.lastCol >= self.worksheet.maxUsedCol:
                self._maxUsedCol = self.worksheet.maxUsedCol
                needToUpdateMaxCol = False
            if self.firstCol <= self.worksheet.minUsedCol:
                self._minUsedCol = self.worksheet.minUsedCol
                needToUpdateMinCol = False
            if self.lastRow >= self.worksheet.maxUsedRow:
                self._maxUsedRow = self.worksheet.maxUsedRow
                needToUpdateMaxRow = False

            if self.firstRow <= self.worksheet.minUsedRow:
                self._minUsedRow = self.worksheet.minUsedRow
                needToUpdateMinRow = False

            if needToUpdateMaxCol or needToUpdateMinCol:
                cIndices = []
                for c in range(self.firstCol, self.lastCol + 1):
                    if self.worksheet.colDict.get(c):
                        cIndices.append(c)
                if cIndices:
                    if needToUpdateMaxCol:
                        self._maxUsedCol = max(cIndices)
                    if needToUpdateMinCol:
                        self._minUsedCol = min(cIndices)

            if needToUpdateMaxRow or needToUpdateMinRow:
                rIndices = []
                for r in range(self.firstRow, self.lastRow + 1):
                    if self.worksheet.rowDict.get(r):
                        rIndices.append(r)
                if rIndices:
                    if needToUpdateMaxRow:
                        self._maxUsedRow = max(rIndices)
                    if needToUpdateMinRow:
                        self._minUsedRow = min(rIndices)
        else:
            self._minUsedCol = None
            self._maxUsedCol = None
            self._minUsedRow = None
            self._maxUsedRow = None


    @property
    def size(self) -> int:
        rt = 0
        for cell in self.worksheet.cells:
            if self.rangeAddress.containCellAddress(cell.address):
                rt += 1
        return rt

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        """take the intersection of this range and the target range, then delete all the cells in that intersection"""
        intersect: RangeAddress | None = self.rangeAddress.intersect(rangeAddress)
        if intersect:
            rs= self.__worksheet.removeRangeRs(intersect)
            self._updateExtremeColRow()
            return rs
        else:
            return Ok(None)

    @staticmethod
    def fromRangeAddress(rangeAddress: RangeAddress, sourceContainer: Worksheet) -> Range:
        return RangeImp(rangeAddress.topLeft, rangeAddress.botRight, sourceContainer)

    @staticmethod
    def fromStrAddress(address: str, sourceContainer: Worksheet) -> Range:
        rangeAddress = RangeAddresses.fromLabel(address)
        return RangeImp.fromRangeAddress(rangeAddress, sourceContainer)

    @staticmethod
    def from2Cells(cell1Address: CellAddress, cell2Address: CellAddress,
                   sourceContainer: Worksheet):
        """ accept any two cells. The cell address can be input in any order """
        rangeAddress = RangeAddresses.from2Cells(cell1Address, cell2Address)
        return RangeImp.fromRangeAddress(rangeAddress, sourceContainer)

    ### >> UserFriendlyCellContainer << ###

    def getCell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        parsedAddress = AddressParser.parseCellAddress(address)
        return self.getOrMakeCell(parsedAddress)

    ### >> CellContainer << ###

    def hasCellAt(self, address: CellAddress) -> bool:
        if self.containsAddress(address):
            return self.__worksheet.hasCellAt(address)
        else:
            return False

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        if self.containsAddressIndex(col, row):
            return self.__worksheet.hasCellAtIndex(col, row)
        else:
            return False

    def getCellAtAddress(self, address: CellAddress) -> Optional[Cell]:
        if self.containsAddress(address):
            return self.__worksheet.getCellAtAddress(address)
        else:
            raise ValueError("cell {cd} is not in range {rd}".format(cd = str(address), rd = str(self.rangeAddress)))

    def isSameRangeAddress(self, other):
        return super().isSameRangeAddress(other)

    @property
    def rangeAddress(self) -> RangeAddressImp:
        return self.__rangeAddress

    ### >> Range  << ###

    @property
    def rootRange(self) -> 'Range':
        return self

    @property
    def worksheet(self) -> Worksheet:
        return self.__worksheet

    @property
    def firstCellAddress(self) -> CellAddress:
        return copy.copy(self.__firstCell)

    @property
    def lastCellAddress(self) -> CellAddress:
        return copy.copy(self.__lastCell)

    @property
    def cells(self) -> list[Cell]:
        allCells = self.__worksheet.cells

        def filterFunction(cell: Cell):
            return self.containsAddress(cell.address)

        rt = list(filter(filterFunction, allCells))
        return rt

    ### >> MutableCellContainer << ###

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        if self.containsAddress(address):
            return WriteBackCell(
                cell = self.__worksheet.getOrMakeCell(address),
                container = self,
                onChange = self.__updateExtremities
            )
            # return self.__sourceContainer.getOrMakeCell(address)
        else:
            raise ValueError("cell {cd} is not in range {rd}".format(cd = str(address), rd = str(self.rangeAddress)))

    def addCell(self, cell: Cell):
        if self.containsAddress(cell.address):
            self.__worksheet.addCell(cell)
            self.__updateExtremities(cell)
        else:
            raise ValueError(
                "Cannot add cell {cd} into range {rd}".format(cd = str(cell.address), rd = str(self.rangeAddress)))

    def __updateExtremities(self, cell: Cell):
        """update extremities"""
        if(self._maxUsedCol and cell.col > self._maxUsedCol) or not self._maxUsedCol:
            self._maxUsedCol = cell.col
        if(self._minUsedCol and cell.col < self._minUsedCol) or not self._minUsedCol :
            self._minUsedCol = cell.col
        if (self._maxUsedRow and cell.row > self._maxUsedRow) or not self._maxUsedRow:
            self._maxUsedRow = cell.row
        if (self._minUsedRow and cell.row < self._minUsedRow) or not self._minUsedRow:
            self._minUsedRow = cell.row

    def removeCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        """only perform deletion if the target cell is within this range, return err otherwise"""
        address = CellAddresses.parse(address)
        if self.containsAddress(address):
            rs = self.__worksheet.removeCellRs(address)
            self._updateExtremeColRow()
            return rs
        else:
            return Err(RangeErrors.CellNotInRangeReport.report(address, self.rangeAddress))
