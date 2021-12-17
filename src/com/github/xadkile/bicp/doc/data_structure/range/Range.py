import copy
from typing import List

from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress
from com.github.xadkile.bicp.doc.data_structure.cell_container.CellContainer import CellContainer
from com.github.xadkile.bicp.doc.data_structure.range.RangeAddress import RangeAddress


class Range(CellContainer):
    """ a sub container derived from bigger cell container """

    @property
    def firstCellAddress(self) -> CellAddress:
       pass

    @property
    def lastCellAddress(self) -> CellAddress:
        pass

    def containsAddress(self, address: CellAddress) -> bool:
        rowIsInRange = self.firstCellAddress.rowIndex <= address.rowIndex <= self.lastCellAddress.rowIndex
        colIsInRange = self.firstCellAddress.colIndex <= address.colIndex <= self.lastCellAddress.colIndex
        return rowIsInRange and colIsInRange