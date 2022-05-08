from abc import ABC
from typing import Tuple

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell_container.CellContainer import CellContainer
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.util.result.Results import Results


class MutableCellContainer(CellContainer, ABC):
    """ container of cells """

    def addCell(self, cell: Cell):
        """add a cell to this container"""
        raise NotImplementedError()

    def deleteCell(self, address: CellAddress | Tuple[int, int] | str):
        delRs = self.deleteCellRs(address)
        return Results.extractOrRaise(delRs)

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        raise NotImplementedError()

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        """
        get cell at an address. If such cell does not exist, return a WriteBackCell
        :return the cell at the position
        """
        raise NotImplementedError()

    def deleteRangeRs(self, rangeAddress:RangeAddress)->Result[None,ErrorReport]:
        raise NotImplementedError()

    def deleteRange(self,rangeAddress:RangeAddress):
        delRs = self.deleteRangeRs(rangeAddress)
        return Results.extractOrRaise(delRs)
