from abc import ABC
from typing import Optional, Union, Tuple

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.util.WithSize import WithSize


class CellContainer(WithSize,ABC):
    """ an immutable cell container. A container support accessing Cells using CellAddress """

    def getCell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Optional[Cell]:
        raise NotImplementedError()
    def getCellAtAddress(self, address: CellAddress) -> Optional[Cell]:
        """
        :return the cell at the position, None of the cell does not exist
        """
        raise NotImplementedError()

    def hasCellAt(self, address: CellAddress) -> bool:
        """
        Important: while this does check for valid address/index, it does NOT return true simply an address/index is inside this container. This check the existence of an object instance inside this container.
        :return true if this container has a cell OBJECT at the specified position
        """
        raise NotImplementedError()

    def hasCellAtIndex(self,col:int, row:int)->bool:
        """
                Important: while this does check for valid address/index, it does NOT return true simply an address/index is inside this container. This check the existence of an object instance inside this container.
                :return true if this container has a cell OBJECT at the specified position
                """
        raise NotImplementedError()

    def containsAddress(self, address: CellAddress) -> bool:
        """ :return true if a CellAddress is within address range of this container """
        raise NotImplementedError()

    def containsAddressIndex(self, col:int, row:int) -> bool:
        """ :return true if a pair of [col,row] is within address range of this container """
        raise NotImplementedError()

    @property
    def cells(self) -> list[Cell]:
        """:return a flat list of cell objects contained in this container"""
        raise NotImplementedError()

    @property
    def rangeAddress(self) -> RangeAddress:
        """:return range address of this container"""
        raise NotImplementedError()

    def isSameRangeAddress(self,other:"CellContainer"):
        """
        :param other:
        :return: true if this container covers the same address as another container, false otherwise
        """
        if isinstance(other,CellContainer):
            return self.rangeAddress == other.rangeAddress
        else:
            raise Exception("Can only compare range address with another CellContainer")