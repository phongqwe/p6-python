from abc import ABC

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell_container.CellContainer import CellContainer


class MutableCellContainer(CellContainer,ABC):
    """ container of cellJsons """

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
