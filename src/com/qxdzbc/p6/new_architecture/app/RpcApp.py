from typing import Union

from com.qxdzbc.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse

from com.qxdzbc.p6.document_structure.app.BaseApp import BaseApp
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.new_architecture.common.RpcUtils import RpcUtils

from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.GetWorkbookRequest import GetWorkbookRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.WorkbookKeyWithErrorResponse import \
    WorkbookKeyWithErrorResponse
from com.qxdzbc.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook


class RpcApp(BaseApp):
    def __init__(
            self,
            rpcStubProvider: RpcStubProvider
    ):
        self.rpcSP = rpcStubProvider

    @property
    def appSv(self):
        return self.rpcSP.appService

    def _onAppSvOk(self, f):
        return RpcUtils.onServiceOk(self.appSv, f)

    def _onAppSvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self.appSv, f)

    def getWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        def f() -> Result[Workbook, ErrorReport]:
            wbk = None
            name = None
            index = None
            if isinstance(key, WorkbookKey):
                wbk = key
            if isinstance(key, str):
                name = key
            if isinstance(key, int):
                index = key
            req = GetWorkbookRequest(
                wbKey = wbk,
                wbName = name,
                wbIndex = index,
            )
            outProto = self.appSv.getWorkbook(request = req.toProtoObj())
            out = WorkbookKeyWithErrorResponse.fromProto(outProto)
            if out.isOk():
                wbKey = out.wbKey
                return Ok(RpcWorkbook(
                    name =wbKey.fileName,
                    path = wbKey.filePath,
                    stubProvider = self.rpcSP
                ))
            else:
                return Err(out.errorReport)
        return self._onAppSvOkRs(f)



