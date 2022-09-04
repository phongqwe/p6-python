import json
from abc import ABC
from typing import Union, Tuple, Optional

from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result

from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto

from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.copy_paste.paster.Paster import Paster
from com.qxdzbc.p6.document_structure.range.Range import Range
from com.qxdzbc.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.document_structure.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.document_structure.util.result.Results import Results
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet


class BaseWorksheet(Worksheet,ABC):


    def paste(self, cell: CellAddress, paster: Paster | None = None):
        rs = self.pasteRs(cell, paster)
        rs.raiseIfErr()

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        if self.minUsedCol and self.maxUsedCol and self.minUsedRow and self.maxUsedRow:
            return RangeAddresses.fromColRow(
                minCol = self.minUsedCol,
                maxCol = self.maxUsedCol,
                minRow = self.minUsedRow,
                maxRow = self.maxUsedRow,
            )
        else:
            return None

    @property
    def usedRange(self) -> Range | None:
        if self.usedRangeAddress:
            return self.range(self.usedRangeAddress)
        else:
            return None

    def pasteDataFrame(self, anchorCell: CellAddress,paster: Paster | None=None):
        rs = self.pasteDataFrameRs(anchorCell,paster)
        Results.extractOrRaise(rs)

    def pasteProto(self, cell: CellAddress, paster: Paster | None = None):
        rs = self.pasteProtoRs(cell, paster)
        rs.raiseIfErr()

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


    def toProtoObj(self) -> WorksheetProto:
        rt = WorksheetProto()
        rt.name = self.name
        cells = []
        for cell in self.cells:
            cells.append(cell.toProtoObj())
        rt.cell.extend(cells)
        return rt

    def removeFromWorkbook(self):
        self.workbook = None


    def reportJsonStr(self) -> str:
        return json.dumps({
            "name": self.name
        })

    def rename(self, newName: str):
        rs = self.renameRs(newName)
        if rs.isErr():
            raise rs.err.toException()

    def cell(self, address: Union[str, CellAddress, Tuple[int, int]]) -> Cell:
        pass

    def range(self, rangeAddress: Union[str, RangeAddress, Tuple[CellAddress, CellAddress]]) -> Range:
        pass

    def deleteCell(self, address: CellAddress | Tuple[int, int] | str):
        return super().deleteCell(address)

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        pass

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        pass

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        pass

    def deleteRange(self, rangeAddress: RangeAddress):
        return super().deleteRange(rangeAddress)

    def hasCellAt(self, address: CellAddress) -> bool:
        pass

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        pass

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        pass

    def containsAddress(self, address: CellAddress) -> bool:
        pass

    def containsAddressIndex(self, col: int, row: int) -> bool:
        pass

    @property
    def cells(self) -> list[Cell]:
        pass

    @property
    def rangeAddress(self) -> RangeAddress:
        pass

    def isSameRangeAddress(self, other: "CellContainer"):
        return super().isSameRangeAddress(other)

    def reRun(self, refreshScript: bool = False):
        super().reRun(refreshScript)

    def isEmpty(self) -> bool:
        return super().isEmpty()

    def isNotEmpty(self) -> bool:
        return super().isNotEmpty()

    def addCell(self, cell: Cell):
        pass





