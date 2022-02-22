from abc import ABC
from typing import Optional, Union, Tuple

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.column.Column import Column
from bicp_document_structure.column.ColumnJson import ColumnJson
from bicp_document_structure.range.Range import Range
from bicp_document_structure.range.address.RangeAddress import RangeAddress


class ColumnWrapper(Column,ABC):

    def __init__(self,innerCol:Column):
        self._innerCol:Column = innerCol

    def range(self, firstRow: int, lastRow: int) -> Range:
        return self._innerCol.range(firstRow, lastRow)

    # @property
    # def _onCellMutationEventHandler(self) -> Callable[[Cell, P6Event], None]:
    #     return self._innerCol._onCellMutationEventHandler

    @property
    def index(self) -> int:
        return self._innerCol.index

    def toJson(self) -> ColumnJson:
        return self._innerCol.toJson()

    @property
    def firstCellAddress(self) -> CellAddress:
        return self._innerCol.firstCellAddress

    @property
    def lastCellAddress(self) -> CellAddress:
        return self._innerCol.lastCellAddress

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        return self._innerCol.cell(address)

    def addCell(self, cell: Cell):
        self._innerCol.addCell(cell)

    def removeCell(self, address: CellAddress):
        self._innerCol.removeCell(address)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        return self._innerCol.getOrMakeCell(address)

    def hasCellAt(self, address: CellAddress) -> bool:
        return self._innerCol.hasCellAt(address)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        return self._innerCol.getCell(address)

    def isEmpty(self) -> bool:
        return self._innerCol.isEmpty()

    @property
    def cells(self) -> list[Cell]:
        return self._innerCol.cells

    @property
    def rangeAddress(self) -> RangeAddress:
        return self._innerCol.rangeAddress