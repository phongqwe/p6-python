from functools import partial
from typing import Optional, Any

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.InternalRpcCell import InternalRpcCell
from com.qxdzbc.p6.cell.WrapperCell import WrapperCell
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.rpc.RpcUtils import RpcUtils
from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.cell.rpc_data_structure.CopyCellRequest import CopyCellRequest
from com.qxdzbc.p6.cell.rpc_data_structure.CellId import CellId
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.rpc.data_structure.StrMsg import StrMsg
from com.qxdzbc.p6.proto.rpc.CellService_pb2_grpc import CellServiceStub


class RpcCell(WrapperCell):

    def __init__(
            self, cellAddress: CellAddress,
            wbKey: WorkbookKey, wsName: str,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()):
        self._ic = InternalRpcCell(
            cellAddress = cellAddress,
            wbKey = wbKey,
            wsName = wsName,
            stubProvider = stubProvider
        )
        super().__init__(self._ic)
        self._address = cellAddress
        self._wbk = wbKey
        self._wsName = wsName
        self._sp = stubProvider

    @staticmethod
    def fromCell(
            cell: Cell,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()):
        return RpcCell(
            cellAddress = cell.address,
            wbKey = cell.wbKey,
            wsName = cell.wsName,
            stubProvider = stubProvider
        )

    @property
    def displayValue(self) -> str:
        def f():
            return self._ic.displayValue
        return self._onCellSvOk(f)

    # @property
    # def formula(self) -> str:
    #     def f():
    #         return self._ic.formula
    #     return self._onCellSvOk(f)
    #
    # @formula.setter
    # def formula(self, newFormula):
    #     super().formula = newFormula
    #     # Cell.formula.fset(self,newFormula)
    #     # def f():
    #     #     self._ic.formula = newFormula
    #     # self._onCellSvOk(f)

    # @property
    # def value(self):
    #     return super().value

    # @value.setter
    # def value(self, newValue:Any):
    #     super().value = newValue
        # def f():
        #     self._ic.value = newValue
        # self._onCellSvOk(f)
        # Cell.value.fset(self,newValue)

    def copyFromRs(self, anotherCell: CellId) -> Result[None, ErrorReport]:
        return self._onCellSvOkRs(partial(self._ic.copyFromRs,anotherCell))

    @property
    def rootCell(self) -> 'Cell':
        return super().rootCell

    @property
    def content(self) -> CellContent:
        def f():
            return self._ic.content
        return self._onCellSvOk(f)

    @content.setter
    def content(self, newContent: CellContent):
        def f():
            self._ic.content = newContent
        self._onCellSvOk(f)

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
            return self._ic.cellValue
        return self._onCellSvOk(f)
