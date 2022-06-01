from abc import ABC

from pandas import DataFrame

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.cell_container.UserFriendlyCellContainer import UserFriendlyCellContainer


class Range(UserFriendlyCellContainer,MutableCellContainer,ABC):
    """ a sub container derived from a bigger cell container """

    @property
    def firstCellAddress(self) -> CellAddress:
       raise NotImplementedError()

    @property
    def lastCellAddress(self) -> CellAddress:
        raise NotImplementedError()

    @property
    def sourceContainer(self)->MutableCellContainer:
        raise NotImplementedError()

    def containsAddress(self, address: CellAddress) -> bool:
        rowIsInRange = self.firstCellAddress.rowIndex <= address.rowIndex <= self.lastCellAddress.rowIndex
        colIsInRange = self.firstCellAddress.colIndex <= address.colIndex <= self.lastCellAddress.colIndex
        return rowIsInRange and colIsInRange

    def __eq__(self, o: object) -> bool:
        if isinstance(o,Range):
            sameRangeAddress = self.isSameRangeAddress(o)
            sameSourceContainer = self.sourceContainer == o.sourceContainer
            return sameSourceContainer and sameRangeAddress
        else:
            return False

    def toPandasDataFrame(self)->DataFrame:
        """create a data frame from a range"""
        