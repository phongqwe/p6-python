from abc import ABC

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer
from bicp_document_structure.cell_container.UserFriendlyCellContainer import UserFriendlyCellContainer


class Range(UserFriendlyCellContainer,MutableCellContainer,ABC):
    """ a sub container derived from a bigger cell container """

    @property
    def firstCellAddress(self) -> CellAddress:
       raise NotImplementedError()

    @property
    def lastCellAddress(self) -> CellAddress:
        raise NotImplementedError()

    def containsAddress(self, address: CellAddress) -> bool:
        rowIsInRange = self.firstCellAddress.rowIndex <= address.rowIndex <= self.lastCellAddress.rowIndex
        colIsInRange = self.firstCellAddress.colIndex <= address.colIndex <= self.lastCellAddress.colIndex
        return rowIsInRange and colIsInRange