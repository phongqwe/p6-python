from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress


class Ranges:
    @staticmethod
    def fromRangeAddress(rangeAddress: RangeAddress, sourceContainer: MutableCellContainer) -> Range:
        return RangeImp.fromRangeAddress(rangeAddress, sourceContainer)

    @staticmethod
    def fromStrAddress(address: str, sourceContainer: MutableCellContainer) -> Range:
        return RangeImp.fromStrAddress(address, sourceContainer)

    @staticmethod
    def from2Cells(firstCellAddress: CellAddress, lastCellAddress: CellAddress,
                   sourceContainer: MutableCellContainer):
        """ accept any two cells. The cell address can be input in any order """
        return RangeImp.from2Cells(firstCellAddress, lastCellAddress, sourceContainer)