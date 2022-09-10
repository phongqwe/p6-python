from typing import Optional

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.rpc.RpcUtils import RpcUtils
from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.rpc.data_structure.cell.CopyCellRequest import CopyCellRequest
from com.qxdzbc.p6.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.rpc.data_structure.StrMsg import StrMsg
from com.qxdzbc.p6.proto.rpc.CellService_pb2_grpc import CellServiceStub


class RpcCell(Cell):

    def __init__(
            self,
            cellAddress: CellAddress,
            wbKey: WorkbookKey,
            wsName: str,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider(),
    ):
        self._address = cellAddress
        self._wbk = wbKey
        self._wsName = wsName
        self._sp = stubProvider

    def copyFromCellRs(self, anotherCell: Cell) -> Result[None, ErrorReport]:
        return self.copyFrom(anotherCell.id)

    @staticmethod
    def fromCell(
            cell:Cell,
            stubProvider:RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()):
        return RpcCell(
            cellAddress = cell.address,
            wbKey = cell.wbKey,
            wsName = cell.wsName,
            stubProvider = stubProvider
        )

    @property
    def displayValue(self) -> str:
        def f() -> str:
            oProto = self._cellSv.getDisplayValue(request = self.id.toProtoObj())
            o = StrMsg.fromProto(oProto)
            return o.v

        return self._onCellSvOk(f)

    @property
    def wsName(self) -> Optional[str]:
        return self._wsName

    @property
    def wbKey(self) -> Optional[WorkbookKey]:
        return self._wbk

    @property
    def formula(self) -> str:
        def f() -> str:
            oProto = self._cellSv.getFormula(request = self.id.toProtoObj())
            o = StrMsg.fromProto(oProto)
            return o.v

        return self._onCellSvOk(f)

    @formula.setter
    def formula(self, newFormula):
        """ set new formula, script will also be updated """
        raise NotImplementedError()

    @property
    def bareValue(self):
        cv: CellValue = self.cellValue
        return cv.value

    @property
    def value(self):
        return self.bareValue

    @value.setter
    def value(self, newValue):
        """ set the value of this cell """
        raise NotImplementedError()

    def isEmpty(self):
        return self.cellValue.isEmpty()

    def copyFromRs(self, anotherCell: CellId) -> Result[None, ErrorReport]:
        def f():
            request = CopyCellRequest(
                fromCell = anotherCell,
                toCell = self.id
            )
            oProto = self._cellSv.copyFrom(request = request.toProtoObj())
            o = SingleSignalResponse.fromProto(oProto)
            return o.toRs()

        return self._onCellSvOkRs(f)

    @property
    def rootCell(self) -> 'Cell':
        return self

    @property
    def content(self) -> CellContent:
        def f() -> CellContent:
            oProto = self._cellSv.getCellContent(request = self.id.toProtoObj())
            o = CellContent.fromProto(oProto)
            return o

        return self._onCellSvOk(f)

    @content.setter
    def content(self, newContent: CellContent):
        raise NotImplementedError()

    @property
    def address(self) -> CellAddress:
        return self._address

    @property
    def _cellSv(self) -> Optional[CellServiceStub]:
        return self._sp.cellService

    def _onCellSvOk(self, f):
        return RpcUtils.onServiceOkOrRaise(self._cellSv, f)

    def _onCellSvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self._cellSv, f)

    @property
    def cellValue(self) -> CellValue:
        def f() -> CellValue:
            oProto = self._cellSv.getCellValue(request = self.id.toProtoObj())
            o = CellValue.fromProto(oProto)
            return o

        return self._onCellSvOk(f)
