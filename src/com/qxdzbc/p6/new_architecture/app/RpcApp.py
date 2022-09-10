from functools import partial
from pathlib import Path
from typing import Union, Optional

from com.qxdzbc.p6.document_structure.app.BaseApp import BaseApp
from com.qxdzbc.p6.document_structure.util.Util import makeGetter
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.new_architecture.app.RpcAppInternal import RpcAppInternal
from com.qxdzbc.p6.new_architecture.common.RpcUtils import RpcUtils
from com.qxdzbc.p6.new_architecture.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.new_architecture.rpc.data_structure.SingleSignalResponse import SingleSignalResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.CreateNewWorkbookRequest import CreateNewWorkbookRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.CreateNewWorkbookResponse import CreateNewWorkbookResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.GetWorkbookRequest import GetWorkbookRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.app.WorkbookKeyWithErrorResponse import \
    WorkbookKeyWithErrorResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.GetWorksheetResponse import GetWorksheetResponse
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.save_wb.SaveWorkbookRequest import SaveWorkbookRequest
from com.qxdzbc.p6.new_architecture.rpc.data_structure.workbook.save_wb.SaveWorkbookResponse import SaveWorkbookResponse
from com.qxdzbc.p6.new_architecture.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.new_architecture.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.proto.CommonProtos_pb2 import EmptyProto


class RpcApp(BaseApp):

    def __init__(
            self,
            rpcStubProvider: RpcStubProvider
    ):
        self.rpcSP = rpcStubProvider
        self.iApp = RpcAppInternal(self.rpcSP)

    def closeWorkbookRs(self, wbKey: WorkbookKey) -> Result[WorkbookKey, ErrorReport]:
        return self._onAppSvOkRs(partial(self.iApp.closeWorkbookRs,wbKey))

    def saveWorkbookAtPathRs(self, wbKey: WorkbookKey, filePath: Union[str,Path]) -> Result[Workbook, ErrorReport]:
        return self._onAppSvOkRs(partial(self.iApp.saveWorkbookAtPathRs,wbKey,filePath))

    @property
    def activeSheet(self) -> Optional[Worksheet]:
        def f():
            return self.iApp.activeSheet
        return self._onAppSvOk(f)

    def setActiveWorkbookRs(self, wbKey: WorkbookKey) -> Result[Workbook, ErrorReport]:
        return self._onAppSvOkRs(partial(self.iApp.setActiveWorkbookRs,wbKey))

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        def f():
            return self.iApp.activeWorkbook
        return self._onAppSvOk(f)


    def createNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        return self._onAppSvOkRs(partial(self.iApp.createNewWorkbookRs,name))
    @property
    def appSv(self):
        return self.rpcSP.appService

    def _onAppSvOk(self, f):
        return RpcUtils.onServiceOkOrRaise(self.appSv, f)

    def _onAppSvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self.appSv, f)

    def getWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        return self._onAppSvOkRs(partial(self.iApp.getWorkbookRs,key))



