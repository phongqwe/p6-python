import copy
from typing import Optional, Union, Tuple

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.range.address.RangeAddressImp import RangeAddressImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.emeraldblast.p6.document_structure.util.AddressParser import AddressParser


class RangeImp(Range):
    """ an immutable sub container of a bigger cell container"""

    def __init__(self, firstCellAddress: CellAddress, lastCellAddress: CellAddress,
                 sourceContainer: MutableCellContainer):

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
                sc=str(sourceContainer.rangeAddress), r=str(rAddress)
            ))

    @staticmethod
    def fromRangeAddress(rangeAddress: RangeAddress, sourceContainer: MutableCellContainer) -> Range:
        return RangeImp(rangeAddress.firstAddress, rangeAddress.lastAddress, sourceContainer)

    @staticmethod
    def fromStrAddress(address: str, sourceContainer: MutableCellContainer) -> Range:
        rangeAddress = RangeAddresses.addressFromLabel(address)
        return RangeImp.fromRangeAddress(rangeAddress,sourceContainer)

    @staticmethod
    def from2Cells(cell1Address: CellAddress, cell2Address: CellAddress,
                   sourceContainer: MutableCellContainer):
        """ accept any two cells. The cell address can be input in any order """
        rangeAddress = RangeAddresses.fromArbitraryCells(cell1Address, cell2Address)
        return RangeImp.fromRangeAddress(rangeAddress, sourceContainer)

    ### >> UserFriendlyCellContainer << ###

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        parsedAddress = AddressParser.parseCellAddress(address)
        return self.getOrMakeCell(parsedAddress)

    ### >> CellContainer << ###

    def containsAddress(self, address: CellAddress) -> bool:
        return super().containsAddress(address)

    def hasCellAt(self, address: CellAddress) -> bool:
        if self.containsAddress(address):
            return self.__sourceContainer.hasCellAt(address)
        else:
            return False

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        if self.containsAddress(address):
            return self.__sourceContainer.getCell(address)
        else:
            raise ValueError("cell {cd} is not in range {rd}".format(cd=str(address), rd=str(self.rangeAddress)))

    def isSameRangeAddress(self, other):
        return super().isSameRangeAddress(other)

    def isEmpty(self) -> bool:
        return super().isEmpty()

    @property
    def rangeAddress(self) -> RangeAddressImp:
        return self.__rangeAddress

    ### >> Range  << ###

    @property
    def sourceContainer(self) -> MutableCellContainer:
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
            raise ValueError("cell {cd} is not in range {rd}".format(cd=str(address), rd=str(self.rangeAddress)))

    def addCell(self, cell: Cell):
        if self.containsAddress(cell.address):
            self.__sourceContainer.addCell(cell)
        else:
            raise ValueError(
                "Cannot add cell {cd} into range {rd}".format(cd=str(cell.address), rd=str(self.rangeAddress)))

    def removeCell(self, address: CellAddress):
        if self.containsAddress(address):
            self.__sourceContainer.removeCell(address)
        else:
            raise ValueError(
                "Cannot remove cell {cd} from range {rd}".format(cd=str(address), rd=str(self.rangeAddress)))
