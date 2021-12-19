import copy
from typing import List

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.RangeAddress import RangeAddress


class RangeImp(Range):
    """ an immutable sub container of a bigger cell container"""

    def __init__(self, firstCellAddress: CellAddress, lastCellAddress: CellAddress,
                 sourceContainer: MutableCellContainer):

        rangeIsValid = sourceContainer.containsAddress(firstCellAddress) and sourceContainer.containsAddress(
            lastCellAddress)
        rAddress = RangeAddress(firstCellAddress, lastCellAddress)
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
    def fromAddress(rangeAddress:RangeAddress,sourceContainer: MutableCellContainer)->Range:
        return RangeImp(rangeAddress.firstAddress,rangeAddress.lastAddress,sourceContainer)

    @staticmethod
    def fromStrAddress(address:str,sourceContainer:MutableCellContainer)->Range:
        raise NotImplementedError()


    ### >> CellContainer << ###

    def hasCellAt(self, address: CellAddress) -> bool:
        if self.containsAddress(address):
            return self.__sourceContainer.hasCellAt(address)
        else:
            return False

    def getCell(self, address: CellAddress) -> Cell:
        if self.containsAddress(address):
            return self.__sourceContainer.getCell(address)
        else:
            raise ValueError("cell {cd} is not in range {rd}".format(cd=str(address), rd=str(self.rangeAddress)))

    def isEmpty(self) -> bool:
        return super().isEmpty()

    @property
    def rangeAddress(self) -> RangeAddress:
        return self.__rangeAddress

    ### >> Range  << ###

    @property
    def firstCellAddress(self) -> CellAddress:
        return copy.copy(self.__firstCell)

    @property
    def lastCellAddress(self) -> CellAddress:
        return copy.copy(self.__lastCell)

    @property
    def cells(self) -> List[Cell]:
        allCells = self.__sourceContainer.cells

        def filterFunction(cell: Cell):
            return self.containsAddress(cell.address)

        rt = list(filter(filterFunction, allCells))
        return rt
