from abc import ABC

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell_container.CellContainer import CellContainer


class MutableCellContainer(CellContainer,ABC):
    """ container of cells """

    def addCell(self, cell: Cell):
        """add a cell to this container"""
        raise NotImplementedError()

    def removeCell(self, address:CellAddress):
        """remove the cell at the specified position"""
        raise NotImplementedError()

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        """
        get cell at an address. If such cell does not exist, return a WriteBackCell
        :return the cell at the position
        """
        raise NotImplementedError()
