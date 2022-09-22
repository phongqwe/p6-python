from functools import partial
from typing import Optional, Tuple

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.IndCell import IndCell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.InternalRpcWorksheet import InternalRpcWorksheet
from com.qxdzbc.p6.worksheet.LoadType import LoadType
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.rpc.RpcUtils import RpcUtils
from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.worksheet.WorksheetWrapper import WorksheetWrapper
from com.qxdzbc.p6.proto.rpc.WorkbookService_pb2_grpc import WorkbookServiceStub
from com.qxdzbc.p6.proto.rpc.WorksheetService_pb2_grpc import WorksheetServiceStub


class RpcWorksheet(WorksheetWrapper):

    def __init__(
            self, name: str, wbKey: WorkbookKey,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()):

        super().__init__(InternalRpcWorksheet(name, wbKey, stubProvider))
        self._stubProvider = stubProvider

    def updateMultipleCellRs(self, updateEntries: list[IndCell]) -> Result[None, ErrorReport]:
        return self._onWsSvOkRs(partial(self.rootWorksheet.updateMultipleCellRs,updateEntries))

    def load2DArrayRs(self, data2DArray, anchorCell: CellAddress = CellAddresses.A1,
                      loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE) -> \
            Result['Worksheet', ErrorReport]:
        return self._onWsSvOkRs(partial(self.rootWorksheet.load2DArrayRs, data2DArray, anchorCell, loadType))

    def loadDataFrameRs(
            self, dataFrame,
            anchorCell: CellAddress = CellAddresses.A1,
            loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE,
            keepHeader: bool = True,
    ) -> Result['Worksheet', ErrorReport]:
        return self._onWsSvOkRs(partial(self.rootWorksheet.loadDataFrameRs,dataFrame,anchorCell,loadType,keepHeader))

    def addCell(self, cell: Cell):
        return self._onWsSvOk(partial(self.rootWorksheet.addCell,cell))

    def removeAllCellRs(self) -> Result[None, ErrorReport]:
        return self._onWsSvOkRs(partial(self.rootWorksheet.removeAllCellRs))

    def removeCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        return self._onWsSvOkRs(partial(self.rootWorksheet.removeCellRs, address))

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        return self._onWsSvOkRs(partial(self.rootWorksheet.deleteRangeRs,rangeAddress))

    def getCellAtAddress(self, address: CellAddress) -> Optional[Cell]:
        return self._onWsSvOk(partial(self.rootWorksheet.getCellAtAddress, address))

    def containsAddress(self, address: CellAddress) -> bool:
        return self._onWsSvOk(partial(self.rootWorksheet.containsAddress,address))

    @property
    def _wbsv(self) -> Optional[WorkbookServiceStub]:
        return self._stubProvider.wbService

    @property
    def _wssv(self) -> Optional[WorksheetServiceStub]:
        return self._stubProvider.wsService

    def _onWsSvOk(self, f):
        return RpcUtils.onServiceOkOrRaise(self._wssv, f)

    def _onWsSvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self._wssv, f)

    def _onWbsvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self._wbsv, f)

    @property
    def size(self) -> int:
        def f() -> int:
            return self.rootWorksheet.size
        return self._onWsSvOk(f)

    @property
    def cells(self) -> list[Cell]:
        def f() -> list[Cell]:
            return self.rootWorksheet.cells
        return self._onWsSvOk(f)

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        def f() -> RangeAddress:
            return self.rootWorksheet.usedRangeAddress
        return self._onWsSvOk(f)

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorksheet.renameRs,newName))

    def pasteRs(self, cell: CellAddress) -> Result[None, ErrorReport]:
        return self._onWsSvOkRs(partial(self.rootWorksheet.pasteRs,cell))
