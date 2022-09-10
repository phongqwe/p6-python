from abc import ABC
from typing import Tuple

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell_container.CellContainer import CellContainer
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.util.result.Results import Results


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
