from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.RangeImp import RangeImp
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class Ranges:
    @staticmethod
    def fromRangeAddress(rangeAddress: RangeAddress, sourceContainer: Worksheet) -> Range:
        return RangeImp.fromRangeAddress(rangeAddress, sourceContainer)

    @staticmethod
    def fromStrAddress(address: str, sourceContainer: Worksheet) -> Range:
        return RangeImp.fromStrAddress(address, sourceContainer)

    @staticmethod
    def from2Cells(firstCellAddress: CellAddress, lastCellAddress: CellAddress,
                   sourceContainer: Worksheet):
        """ accept any two cells. The cell address can be input in any order """
        return RangeImp.from2Cells(firstCellAddress, lastCellAddress, sourceContainer)