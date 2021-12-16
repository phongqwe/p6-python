from typing import List

from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress
from com.github.xadkile.bicp.doc.data_structure.range.RangeAddress import RangeAddress


class CellContainer:
    """ an immutable cell container """
    def hasCellAt(self, address:CellAddress)->bool:
        """
        Important: while this does check for valid address/index, it does NOT return true simply an address/index is inside this container. This check the existence of an object instance inside this container.
        :return true if this holder has a cell OBJECT at the specified position
        """
        pass

    # def containsAddress(self):

    def getCell(self, address:CellAddress) -> Cell:
        """
        get cell at an address. If such cell does not exist, return a TempCell
        :return the cell at the position
        """
        pass

    def isEmpty(self) -> bool:
        """:return true if this holder is empty"""
        pass

    def containsAddress(self, address:CellAddress)->bool:
        """ :return true if a CellPosition is within position range of this container """
        pass

    @property
    def cells(self)->List[Cell]:
        """:return a flat list of cell objects contained in this container"""
        pass

    @property
    def rangeAddress(self)->RangeAddress:
        """:return range address of this container"""
        pass