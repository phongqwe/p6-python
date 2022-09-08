import json
from abc import ABC
from typing import Union, Tuple, Optional

from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.cell_container.CellContainer import CellContainer
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result

from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto

from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.range.Range import Range
from com.qxdzbc.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.result.Results import Results
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet


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
        if sameName:
            sameCellCount = ws1.cellCount == ws1.cellCount
            if sameCellCount:
                z = True
                for c1 in ws1.cells:
                    c2 = ws2.cell(c1.address)
                    if c1 != c2:
                        return False

                for c2 in ws2.cells:
                    c1 = ws1.cell(c2.address)
                    if c2 != c1:
                        return False
                return z
            else:
                return False
        else:
            return False

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
