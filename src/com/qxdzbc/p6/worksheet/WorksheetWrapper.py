from typing import Optional, Tuple

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.BaseWorksheet import BaseWorksheet
from com.qxdzbc.p6.worksheet.LoadType import LoadType
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.worksheet.rpc_data_structure import WorksheetId


class WorksheetWrapper(BaseWorksheet):

    def __init__(self, innerWorksheet: Worksheet):
        self._innerSheet: Worksheet = innerWorksheet

    def addCellRs(self, cell: Cell) -> Result[None, ErrorReport]:
        return self.rootWorksheet.addCellRs(cell)

    @property
    def id(self) -> WorksheetId:
        return self.rootWorksheet.id

    def load2DArrayRs(self, dataAray, anchorCell: CellAddress = CellAddresses.A1,
                      loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE) -> Result['Worksheet', ErrorReport]:
        return self.rootWorksheet.load2DArrayRs(dataAray, anchorCell, loadType)

    def loadDataFrameRs(
            self, dataFrame,
            anchorCell: CellAddress = CellAddresses.A1,
            loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE,
            keepHeader: bool = True,
    ) -> Result['Worksheet', ErrorReport]:
        return self.loadDataFrameRs(dataFrame, anchorCell, loadType)

    def toProtoObj(self) -> WorksheetProto:
        return self.rootWorksheet.toProtoObj()

    @property
    def wbKey(self) -> WorkbookKey:
        return self.rootWorksheet.wbKey

    def pasteRs(self, cell: CellAddress) -> Result[None, ErrorReport]:
        return self.rootWorksheet.pasteRs(cell)

    @property
    def maxUsedCol(self) -> int | None:
        return self.rootWorksheet.maxUsedCol

    @property
    def minUsedCol(self) -> int | None:
        return self.rootWorksheet.minUsedCol

    @property
    def maxUsedRow(self) -> int | None:
        return self.rootWorksheet.maxUsedRow

    @property
    def minUsedRow(self) -> int | None:
        return self.rootWorksheet.minUsedRow

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        return self.rootWorksheet.usedRangeAddress

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        return self.rootWorksheet.hasCellAtIndex(col, row)

    def containsAddressIndex(self, col: int, row: int) -> bool:
        return self.rootWorksheet.containsAddressIndex(col, row)

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        return self.rootWorksheet.deleteRangeRs(rangeAddress)

    def removeCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        return self.rootWorksheet.removeCellRs(address)

    @property
    def rootWorksheet(self) -> 'Worksheet':
        return self._innerSheet.rootWorksheet

    @property
    def name(self) -> str:
        return self.rootWorksheet.name

    @property
    def size(self) -> int:
        return self.rootWorksheet.size

    def cell(self, address: str | CellAddress | Tuple[int, int]) -> Cell:
        return self.rootWorksheet.cell(address)

    def range(self, rangeAddress: str | RangeAddress | Tuple[CellAddress, CellAddress]) -> Range:
        return self.rootWorksheet.range(rangeAddress)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        return self.rootWorksheet.getOrMakeCell(address)

    def hasCellAt(self, address: CellAddress) -> bool:
        return self.rootWorksheet.hasCellAt(address)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        return self.rootWorksheet.getCell(address)

    def containsAddress(self, address: CellAddress) -> bool:
        return self.rootWorksheet.containsAddress(address)

    @property
    def cells(self) -> list[Cell]:
        return self.rootWorksheet.cells

    @property
    def rangeAddress(self) -> RangeAddress:
        return self.rootWorksheet.rangeAddress

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        return self.rootWorksheet.renameRs(newName)
