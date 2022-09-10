from abc import ABC
from typing import Tuple

from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.util.result import Results
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


class BaseWorksheet(Worksheet,ABC):

    def paste(self, cell: CellAddress):
        rs = self.pasteRs(cell)
        rs.raiseIfErr()

    @property
    def usedRange(self) -> Range | None:
        if self.usedRangeAddress:
            return self.range(self.usedRangeAddress)
        else:
            return None

    def pasteDataFrame(self, anchorCell: CellAddress,dataFrame):
        rs = self.pasteDataFrameRs(anchorCell,dataFrame)
        Results.extractOrRaise(rs)

    def compareContent(self, ws2: Worksheet) -> bool:
        """compare all cell of this sheet with another. Very inefficient, use with care"""
        ws1 = self.rootWorksheet
        ws2 = ws2.rootWorksheet
        sameName = ws1.name == ws2.name
        sameWb = ws1.wbKey == ws2.wbKey
        return sameName and sameWb


    @property
    def cellCount(self):
        return self.size


    # def toProtoObj(self) -> WorksheetProto:
    #     rt = WorksheetProto()
    #     rt.name = self.name
    #     cells = []
    #     for cell in self.cells:
    #         cells.append(cell.toProtoObj())
    #     rt.cell.extend(cells)
    #     return rt


    def rename(self, newName: str):
        rs = self.renameRs(newName)
        if rs.isErr():
            raise rs.err.toException()

    def deleteCell(self, address: CellAddress | Tuple[int, int] | str):
        return self.deleteCellRs(address)
