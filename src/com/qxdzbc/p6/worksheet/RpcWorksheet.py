from functools import partial
from typing import Optional, Union, Tuple

import numpy
import pandas

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.CellProtoMapping import CellProtoMapping
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.address.CellAddresses import CellAddresses
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.range.address.RangeAddresses import RangeAddresses
from com.qxdzbc.p6.util.CommonError import CommonErrors
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.BaseWorksheet import BaseWorksheet
from com.qxdzbc.p6.worksheet.InternalRpcWorksheet import InternalRpcWorksheet
from com.qxdzbc.p6.worksheet.LoadType import LoadType
from com.qxdzbc.p6.worksheet.WorksheetProtoMapping import WorksheetProtoMapping
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.rpc.RpcUtils import RpcUtils
from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.cell.RpcCell import RpcCell
from com.qxdzbc.p6.rpc.data_structure.BoolMsg import \
    BoolMsg
from com.qxdzbc.p6.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.worksheet.WorksheetWrapper import WorksheetWrapper
from com.qxdzbc.p6.worksheet.rpc_data_structure.LoadDataRequest import LoadDataRequest
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetId import WorksheetId
from com.qxdzbc.p6.rpc.data_structure.range.RangeId import RangeId
from com.qxdzbc.p6.rpc.data_structure.workbook.RenameWorksheetRequest import RenameWorksheetRequest
from com.qxdzbc.p6.range.RpcRange import RpcRange
from com.qxdzbc.p6.worksheet.rpc_data_structure.CellCountResponse import CellCountResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.CheckContainAddressRequest import CheckContainAddressRequest
from com.qxdzbc.p6.worksheet.rpc_data_structure.GetAllCellResponse import GetAllCellResponse
from com.qxdzbc.p6.worksheet.rpc_data_structure.GetUsedRangeResponse import GetUsedRangeResponse
from com.qxdzbc.p6.proto.CommonProtos_pb2 import SingleSignalResponseProto
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto
from com.qxdzbc.p6.proto.rpc.WorkbookService_pb2_grpc import WorkbookServiceStub
from com.qxdzbc.p6.proto.rpc.WorksheetService_pb2_grpc import WorksheetServiceStub


class RpcWorksheet(WorksheetWrapper):

    def __init__(
            self, name: str, wbKey: WorkbookKey,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()):

        super().__init__(InternalRpcWorksheet(name, wbKey, stubProvider))
        self._stubProvider = stubProvider

    def load2DArrayRs(self, dataAray, anchorCell: CellAddress = CellAddresses.A1,
                      loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE) -> \
            Result['Worksheet', ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorksheet.load2DArrayRs, dataAray, anchorCell, loadType))

    def loadDataFrameRs(
            self, dataFrame,
            anchorCell: CellAddress = CellAddresses.A1,
            loadType: LoadType = LoadType.KEEP_OLD_DATA_IF_COLLIDE,
            keepHeader: bool = True,
    ) -> Result['Worksheet', ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorksheet.loadDataFrameRs,dataFrame,anchorCell,loadType,keepHeader))

    def addCell(self, cell: Cell):
        return self._onWsSvOk(partial(self.rootWorksheet.addCell,cell))

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorksheet.deleteCellRs,address))

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        return self._onWbsvOkRs(partial(self.rootWorksheet.deleteRangeRs,rangeAddress))

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        return self._onWsSvOk(partial(self.rootWorksheet.getCell,address))

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
        return self._onWsSvOk(partial(self.rootWorksheet.pasteRs,cell))
