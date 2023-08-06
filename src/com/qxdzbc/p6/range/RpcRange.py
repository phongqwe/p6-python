from functools import partial
from typing import Optional

from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.proto.rpc.WorksheetService_pb2_grpc import WorksheetServiceStub
from com.qxdzbc.p6.range.InternalRpcRange import InternalRpcRange
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.RangeWrapper import RangeWrapper
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.rpc.RpcUtils import RpcUtils
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey


class RpcRange(RangeWrapper):
    def __init__(
            self, rangeAddress: RangeAddress,
            wbKey: WorkbookKey,
            wsName: str,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()
    ):
        innerRange: Range = InternalRpcRange(rangeAddress, wbKey, wsName,stubProvider)
        super().__init__(innerRange)
        self._address = rangeAddress
        self._wbk = wbKey
        self._wsName = wsName
        self._sp = stubProvider

    @property
    def _wssv(self) -> Optional[WorksheetServiceStub]:
        return self._sp.wsService

    # def _onWsSvOk(self, f):
    #     return RpcUtils.onServiceOkOrRaise(self._wssv, f)

    def _onWsSvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self._wssv, f)

    def assign2dArrayRs(self, data2DArray) -> Result[None, ErrorReport]:
        return self._onWsSvOkRs(partial(
            self.rootRange.assign2dArrayRs, data2DArray
        ))