from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.RangeImp import RangeImp
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


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