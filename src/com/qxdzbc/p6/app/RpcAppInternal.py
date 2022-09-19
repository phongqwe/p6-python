from pathlib import Path
from typing import Union, Optional

from com.qxdzbc.p6.app.BaseApp import BaseApp
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.rpc.data_structure.BoolMsg import BoolMsg
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import SingleSignalResponse
from com.qxdzbc.p6.app.rpc_data_structure.CreateNewWorkbookRequest import CreateNewWorkbookRequest
from com.qxdzbc.p6.app.rpc_data_structure.CreateNewWorkbookResponse import CreateNewWorkbookResponse
from com.qxdzbc.p6.app.rpc_data_structure.GetAllWorkbookResponse import GetAllWorkbookResponse
from com.qxdzbc.p6.app.rpc_data_structure.GetWorkbookRequest import GetWorkbookRequest
from com.qxdzbc.p6.app.rpc_data_structure.LoadWorkbookRequest import LoadWorkbookRequest
from com.qxdzbc.p6.app.rpc_data_structure.LoadWorkbookResponse import LoadWorkbookResponse
from com.qxdzbc.p6.app.rpc_data_structure.WorkbookKeyWithErrorResponse import \
    WorkbookKeyWithErrorResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.GetWorksheetResponse import GetWorksheetResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.save_wb.SaveWorkbookRequest import SaveWorkbookRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.save_wb.SaveWorkbookResponse import SaveWorkbookResponse
from com.qxdzbc.p6.workbook.RpcWorkbook import RpcWorkbook
from com.qxdzbc.p6.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.proto.CommonProtos_pb2 import EmptyProto


class RpcAppInternal(BaseApp):

    @property
    def workbooks(self) -> list[Workbook]:
        oProto = self.appSv.getAllWorkbooks(request=EmptyProto())
        o:GetAllWorkbookResponse = GetAllWorkbookResponse.fromProto(oProto)
        rt = list(map(lambda wbk: RpcWorkbook(wbKey = wbk,stubProvider = self.rpcSP),o.wbKeys))
        return rt

    def hasWorkbook(self, wbKey: WorkbookKey) -> bool:
        oProto = self.appSv.checkWbExistence(request=wbKey.toProtoObj())
        o = BoolMsg.fromProto(oProto)
        return o.v

    def loadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        req = LoadWorkbookRequest(
            path = str(filePath)
        )
        oProto = self.appSv.loadWorkbook(request=req.toProtoObj())
        o:LoadWorkbookResponse = LoadWorkbookResponse.fromProto(oProto)
        if o.wbKey:
            return Ok(RpcWorkbook(wbKey = o.wbKey,stubProvider = self.rpcSP))
        else:
            return Err(o.errorReport)

    def closeWorkbookByWbKeyRs(self, wbKey: WorkbookKey) -> Result[WorkbookKey, ErrorReport]:
        oProto = self.appSv.closeWorkbook(request=wbKey.toProtoObj())
        o = SingleSignalResponse.fromProto(oProto)
        if o.isOk():
            return Ok(wbKey)
        else:
            return Err(o.errorReport)


    def saveWorkbookAtPathRs(self, wbKey: WorkbookKey, filePath: Union[str,Path]) -> Result[Workbook, ErrorReport]:
        p = filePath
        if isinstance(p, Path):
            p = str(filePath.absolute())

        req = SaveWorkbookRequest(
            wbKey = wbKey, path = p
        )
        oProto = self.appSv.saveWorkbookAtPath(request = req.toProtoObj())
        o = SaveWorkbookResponse.fromProto(oProto)
        if o.wbKey:
            return Ok(RpcWorkbook(wbKey = o.wbKey, stubProvider = self.rpcSP))
        else:
            return Err(o.errorReport)
    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        oProto = self.appSv.getActiveWorksheet(request = EmptyProto())
        o:GetWorksheetResponse = GetWorksheetResponse.fromProto(oProto)
        wsId = o.wsId
        if wsId:
            return RpcWorksheet(
                name = wsId.wsName,
                wbKey = wsId.wbKey,
                stubProvider = self.rpcSP
            )
        else:
            return None

    def setActiveWorkbookRs(self, wbKey: WorkbookKey) -> Result[Workbook, ErrorReport]:
        oProto = self.appSv.setActiveWorkbook(request=wbKey.toProtoObj())
        o = SingleSignalResponse.fromProto(oProto)
        rs:Result[None,ErrorReport] = o.toRs()
        if rs.isOk():
            return Ok(RpcWorkbook(wbKey = wbKey))
        else:
            return Err(rs.err)

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        req = EmptyProto()
        oProto = self.appSv.getActiveWorkbook(request = req)
        o: WorkbookKeyWithErrorResponse = WorkbookKeyWithErrorResponse.fromProto(oProto)
        if o.errorReport:
            return None
        if o.wbKey:
            return RpcWorkbook(
                wbKey = o.wbKey
            )
    def __init__(
            self,
            rpcStubProvider: RpcStubProvider
    ):
        self.rpcSP = rpcStubProvider

    def createNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        req = CreateNewWorkbookRequest(
            workbookName = name
        )
        oProto = self.appSv.createNewWorkbook(request=req.toProtoObj())
        o:CreateNewWorkbookResponse = CreateNewWorkbookResponse.fromProto(oProto)
        if o.errorReport:
            return Err(o.errorReport)
        if o.wbKey:
            return Ok(RpcWorkbook(
                wbKey = o.wbKey,
            ))

    @property
    def appSv(self):
        return self.rpcSP.appService

    def getWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
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
                wbKey =wbKey,
                stubProvider = self.rpcSP
            ))
        else:
            return Err(out.errorReport)