from abc import ABC

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell_container.CellContainer import CellContainer
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.util.result.Results import Results


class MutableCellContainer(CellContainer,ABC):
    """ container of cells """

    def addCell(self, cell: Cell):
        """add a cell to this container"""
        raise NotImplementedError()

    def deleteCell(self, address:CellAddress):
        delRs = self.deleteCellRs(address)
        return Results.extractOrRaise(delRs)

    def deleteCellRs(self,address:CellAddress)->Result[None,ErrorReport]:
        raise NotImplementedError()

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        """
        get cell at an address. If such cell does not exist, return a WriteBackCell
        :return the cell at the position
        """
        raise NotImplementedError()
