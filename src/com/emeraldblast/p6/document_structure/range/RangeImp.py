import copy
from typing import Optional, Union, Tuple

from pandas import DataFrame

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.address.CellAddresses import CellAddresses
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.RangeErrors import RangeErrors
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.AddressParser import AddressParser
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


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
            self.__sourceContainer = sourceContainer
        else:
            raise ValueError("container {sc} does not contain range {r}".format(
                sc = str(sourceContainer.rangeAddress), r = str(rAddress)
            ))

    @property
    def size(self) -> int:
        rt=0
        for cell in self.worksheet.cells:
            if self.rangeAddress.containCellAddress(cell.address):
                rt+=1
        return rt

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        intersect: RangeAddress | None = self.rangeAddress.findIntersection(rangeAddress)
        if intersect:
            return self.__sourceContainer.deleteRangeRs(intersect)
        else:
            return Ok(None)

    @staticmethod
    def fromRangeAddress(rangeAddress: RangeAddress, sourceContainer: MutableCellContainer) -> Range:
        return RangeImp(rangeAddress.topLeft, rangeAddress.botRight, sourceContainer)

    @staticmethod
    def fromStrAddress(address: str, sourceContainer: MutableCellContainer) -> Range:
        rangeAddress = RangeAddresses.fromLabel(address)
        return RangeImp.fromRangeAddress(rangeAddress, sourceContainer)

    @staticmethod
    def from2Cells(cell1Address: CellAddress, cell2Address: CellAddress,
                   sourceContainer: MutableCellContainer):
        """ accept any two cells. The cell address can be input in any order """
        rangeAddress = RangeAddresses.from2Cells(cell1Address, cell2Address)
        return RangeImp.fromRangeAddress(rangeAddress, sourceContainer)

    ### >> UserFriendlyCellContainer << ###

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        parsedAddress = AddressParser.parseCellAddress(address)
        return self.getOrMakeCell(parsedAddress)

    ### >> CellContainer << ###

    def containsAddress(self, address: CellAddress) -> bool:
        return super().containsAddress(address)

    def containsAddressIndex(self, col: int, row: int) -> bool:
        return super().containsAddressIndex(col, row)

    def hasCellAt(self, address: CellAddress) -> bool:
        if self.containsAddress(address):
            return self.__sourceContainer.hasCellAt(address)
        else:
            return False

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        if self.containsAddressIndex(col,row):
            return self.__sourceContainer.hasCellAtIndex(col, row)
        else:
            return False

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        if self.containsAddress(address):
            return self.__sourceContainer.getCell(address)
        else:
            raise ValueError("cell {cd} is not in range {rd}".format(cd = str(address), rd = str(self.rangeAddress)))

    def isSameRangeAddress(self, other):
        return super().isSameRangeAddress(other)

    def isEmpty(self) -> bool:
        return super().isEmpty()

    @property
    def rangeAddress(self) -> RangeAddressImp:
        return self.__rangeAddress

    ### >> Range  << ###

    @property
    def rootRange(self) -> 'Range':
        return self

    @property
    def worksheet(self) -> Worksheet:
        return self.__sourceContainer

    @property
    def firstCellAddress(self) -> CellAddress:
        return copy.copy(self.__firstCell)

    @property
    def lastCellAddress(self) -> CellAddress:
        return copy.copy(self.__lastCell)

    @property
    def cells(self) -> list[Cell]:
        allCells = self.__sourceContainer.cells

        def filterFunction(cell: Cell):
            return self.containsAddress(cell.address)

        rt = list(filter(filterFunction, allCells))
        return rt

    ### >> MutableCellContainer << ###

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        if self.containsAddress(address):
            return self.__sourceContainer.getOrMakeCell(address)
        else:
            raise ValueError("cell {cd} is not in range {rd}".format(cd = str(address), rd = str(self.rangeAddress)))

    def addCell(self, cell: Cell):
        if self.containsAddress(cell.address):
            self.__sourceContainer.addCell(cell)
        else:
            raise ValueError(
                "Cannot add cell {cd} into range {rd}".format(cd = str(cell.address), rd = str(self.rangeAddress)))

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        address = CellAddresses.parseAddress(address)
        if self.containsAddress(address):
            return self.__sourceContainer.deleteCellRs(address)
        else:
            return Err(RangeErrors.CellNotInRangeReport(address, self.rangeAddress))
