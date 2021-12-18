from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell_container.CellContainer import CellContainer


class MutableCellContainer(CellContainer):
    """ container of cells """

    def addCell(self, cell: Cell):
        """add a cell to this container"""
        pass

    def removeCell(self, address:CellAddress):
        """remove the cell at the specified position"""
        pass