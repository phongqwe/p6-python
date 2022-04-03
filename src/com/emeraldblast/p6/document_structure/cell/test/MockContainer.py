from typing import Optional

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress


class MockCellContainer(MutableCellContainer):
    def __init__(self):
        self._l = {}

    def addCell(self, cell: Cell):
        self._l[cell.address] = cell

    def removeCell(self, address: CellAddress):
        del self._l[address]

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        pass

    def hasCellAt(self, address: CellAddress) -> bool:
        return self.getCell(address) is not None

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        try:
            z = self._l[address]
            return z
        except:
            return None

    def isEmpty(self) -> bool:
        pass

    def containsAddress(self, address: CellAddress) -> bool:
        return self.getCell(address) is not None

    @property
    def cells(self) -> list[Cell]:
        return list(self._l.values())

    @property
    def rangeAddress(self) -> RangeAddress:
        return None

    def isSameRangeAddress(self, other):
        return False
