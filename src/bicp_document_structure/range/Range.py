from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell_container.CellContainer import CellContainer


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