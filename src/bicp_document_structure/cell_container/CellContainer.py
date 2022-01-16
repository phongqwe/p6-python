from abc import ABC
from typing import List, Optional

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.range.address.RangeAddress import RangeAddress


class CellContainer(ABC):
    """ an immutable cell container. A container support accessing Cells using CellAddress """

    def hasCellAt(self, address: CellAddress) -> bool:
        """
        Important: while this does check for valid address/index, it does NOT return true simply an address/index is inside this container. This check the existence of an object instance inside this container.
        :return true if this container has a cell OBJECT at the specified position
        """
        raise NotImplementedError()

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        """
        :return the cell at the position
        """
        raise NotImplementedError()

    def isEmpty(self) -> bool:
        """:return true if this container is empty"""
        raise NotImplementedError()

    def containsAddress(self, address: CellAddress) -> bool:
        """ :return true if a CellAddress is within address range of this container """
        raise NotImplementedError()

    @property
    def cells(self) -> List[Cell]:
        """:return a flat list of cell objects contained in this container"""
        raise NotImplementedError()

    @property
    def rangeAddress(self) -> RangeAddress:
        """:return range address of this container"""
        raise NotImplementedError()

    def isSameRangeAddress(self,other):
        """
        :param other:
        :return: true if this container covers the same address as another container, false otherwise
        """
        if isinstance(other,CellContainer):
            return self.rangeAddress == other.rangeAddress
        else:
            return False
