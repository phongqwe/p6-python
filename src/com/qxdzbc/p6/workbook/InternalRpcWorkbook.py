from pathlib import Path
from typing import Union, Optional

from com.qxdzbc.p6.util.CommonError import CommonErrors
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.util.result.Results import Results
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.WorkbookErrors import WorkbookErrors
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.workbook.key.WorkbookKeys import WorkbookKeys
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.rpc.RpcUtils import RpcUtils
from com.qxdzbc.p6.di.RpcServiceContainer import RpcServiceContainer
from com.qxdzbc.p6.rpc.RpcErrors import RpcErrors
from com.qxdzbc.p6.rpc.RpcValues import RpcValues
from com.qxdzbc.p6.rpc.StubProvider import RpcStubProvider
from com.qxdzbc.p6.rpc.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.AddWorksheetRequest import AddWorksheetRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.GetAllWorksheetsResponse import \
    GetAllWorksheetsResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.GetWorksheetResponse import GetWorksheetResponse
from com.qxdzbc.p6.workbook.rpc_data_structure.RenameWorksheetRequest import \
    RenameWorksheetRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.SetWbNameRequest import SetWbNameRequest
from com.qxdzbc.p6.workbook.rpc_data_structure.WorksheetWithErrorReportMsg import \
    WorksheetWithErrorReportMsg
from com.qxdzbc.p6.worksheet.rpc_data_structure.WorksheetIdWithIndex import WorksheetIdWithIndex
from com.qxdzbc.p6.worksheet.RpcWorksheet import RpcWorksheet
from com.qxdzbc.p6.proto.CommonProtos_pb2 import SingleSignalResponseProto
from com.qxdzbc.p6.proto.WorksheetProtos_pb2 import GetWorksheetResponseProto
from com.qxdzbc.p6.proto.WorkbookProtos_pb2 import WorksheetWithErrorReportMsgProto
from com.qxdzbc.p6.proto.rpc.WorkbookService_pb2_grpc import WorkbookServiceStub


class InternalRpcWorkbook(Workbook):
    _serverDownReport = RpcErrors.RpcServerIsDown \
        .report("Can't call rpc because rpc server is down.")
    _serverDownException = _serverDownReport.toException()

    def __init__(
            self,
            wbKey:WorkbookKey,
            stubProvider: RpcStubProvider = RpcServiceContainer.insecureRpcServiceProvider()
    ):
        self.__key = wbKey
        self._stubProvider = stubProvider

    def __eq__(self, o: object) -> bool:
        if isinstance(o,Workbook):
            return self.key == o.key
        else:
            return False

    def removeAllWorksheetRs(self) -> Result[None, ErrorReport]:
        oProto = self._wbsv.removeAllWorksheet(request = self.key.toProtoObj())
        o = SingleSignalResponse.fromProto(oProto)
        return o.toRs()

    def setStubProvider(self, stubProvider: RpcStubProvider):
        self._stubProvider = stubProvider

    @property
    def _wbsv(self) -> Optional[WorkbookServiceStub]:
        return self._stubProvider.wbService

    ### >> Workbook << ###

    @property
    def worksheets(self) -> list[Worksheet]:
        outProto = self._wbsv.getAllWorksheets(self.key.toProtoObj())
        out = GetAllWorksheetsResponse.fromProto(outProto)
        return out.worksheets

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[None, ErrorReport]:
        if isinstance(indexOrName, int):
            return self.setActiveWorksheetByIndexRs(indexOrName)
        elif isinstance(indexOrName, str):
            return self.setActiveWorksheetByNameRs(indexOrName)
        else:
            return Err(CommonErrors.WrongTypeReport("nameOrIndex", "str or int"))

    def setActiveWorksheetByNameRs(self, name: str) -> Result[None, ErrorReport]:
        request = WorksheetIdWithIndex(
            wbKey = self.key,
            wsName = name
        )
        return self.setActiveWsRpcRs(request)

    def setActiveWorksheetByIndexRs(self, index: int) -> Result[None, ErrorReport]:
        request = WorksheetIdWithIndex(
            wbKey = self.key,
            wsIndex = index,
        )
        return self.setActiveWsRpcRs(request)

    def setActiveWsRpcRs(self, request: WorksheetIdWithIndex) -> Result[None, ErrorReport]:
        outProto: SingleSignalResponseProto = self._wbsv.setActiveWorksheet(
            request = request.toProtoObj())
        out = SingleSignalResponse.fromProto(outProto)
        if out.isError():
            return Err(out.errorReport)
        else:
            return Ok(None)

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        wbsv = self._wbsv
        outProto: GetWorksheetResponseProto = wbsv.getActiveWorksheet(self.key.toProtoObj())
        out = GetWorksheetResponse.fromProto(outProto)
        wsId =out.wsId
        if wsId:
            return RpcWorksheet(
                name =wsId.wsName,
                wbKey = wsId.wbKey,
                stubProvider = self._stubProvider
            )
        else:
            return None

    def isEmpty(self) -> bool:
        return self.sheetCount == 0

    def _onWbsvOkRs(self, f):
        return RpcUtils.onServiceOkRs(self._wbsv,f)


    def _makeGetWsRpcRequestRs(self, request: WorksheetIdWithIndex) -> Result[Worksheet, ErrorReport]:
        def errorMsg(index, name) -> str:
            if name:
                return f"Worksheet \"{name}\" does not exist"
            if index:
                return f"Worksheet at index \"{index}\" does not exist"
            else:
                raise CommonErrors.WrongTypeReport("nameOrIndex", "str or int").toException()

        def f():
            outProto: GetWorksheetResponseProto = self._wbsv.getWorksheet(request = request.toProtoObj())
            out:GetWorksheetResponse = GetWorksheetResponse.fromProto(outProto)
            wsId = out.wsId

            if wsId:
                return Ok(wsId)
            else:
                return Err(WorkbookErrors.WorksheetNotExistReport.report(errorMsg(request.wsIndex, request.wsName)))

        return self._onWbsvOkRs(f)

    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        req = WorksheetIdWithIndex(
            wbKey = self.key,
            wsName = name
        )
        return self._makeGetWsRpcRequestRs(req)

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        req = WorksheetIdWithIndex(
            wbKey = self.key,
            wsIndex = index
        )
        return self._makeGetWsRpcRequestRs(req)

    def getWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        if isinstance(nameOrIndex, str):
            return self.getWorksheetByNameRs(nameOrIndex)
        elif isinstance(nameOrIndex, int):
            return self.getWorksheetByIndexRs(nameOrIndex)
        else:
            return Err(CommonErrors.WrongTypeReport("nameOrIndex", "str or int"))

    @property
    def sheetCount(self) -> int:
        if self._wbsv is not None:
            out: RpcValues.Int64Value = self._wbsv.sheetCount(
                request = self.key.toProtoObj()
            )
            return out.value
        else:
            raise InternalRpcWorkbook._serverDownException

    @property
    def path(self) -> Path:
        return self.key.filePath

    @path.setter
    def path(self, newPath: Path):
        self.key = WorkbookKeys.fromNameAndPath(self.name, newPath)

    @property
    def name(self) -> str:
        return self.key.fileName

    @property
    def key(self) -> WorkbookKey:
        return self.__key

    @key.setter
    def key(self, newKey: WorkbookKey):
        if self._wbsv is not None:
            if newKey == self.__key:
                return
            else:
                outProto = self._wbsv.setWbKey(
                    request = SetWbNameRequest(
                        wbKey = self.__key,
                        newWbKey = newKey
                    ).toProtoObj()
                )
                out: SingleSignalResponse = SingleSignalResponse.fromProto(outProto)
                err = out.errorReport
                if err is not None:
                    raise err.toException()
                else:
                    self.__key = newKey
        else:
            raise InternalRpcWorkbook._serverDownException

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        req = CreateNewWorksheetRequest(
            wbKey = self.__key,
            newWorksheetName = newSheetName
        ).toProtoObj()
        outProto: WorksheetWithErrorReportMsgProto = self._wbsv.createNewWorksheet(request = req)
        out = WorksheetWithErrorReportMsg.fromProto(outProto)
        if out.isErr():
            return Err(out.errorReport)
        else:
            ws = RpcWorksheet(
                name=out.wsName,
                wbKey = self.__key,
                stubProvider =self._stubProvider
            )
            return Ok(ws)


    def _deleteWorksheetRsRpc(self, request: WorksheetIdWithIndex) -> Result[None, ErrorReport]:
        req = request.toProtoObj()
        outProto: SingleSignalResponseProto = self._wbsv.deleteWorksheet(request = req)
        out = SingleSignalResponse.fromProto(outProto)
        return out.toRs()

    def removeWorksheetByNameRs(self, sheetName: str) -> Result[None, ErrorReport]:
        req = WorksheetIdWithIndex(
            wbKey = self.__key,
            wsName = sheetName
        )
        return self._deleteWorksheetRsRpc(req)

    def removeWorksheetByIndexRs(self, index: int) -> Result[None, ErrorReport]:
        req = WorksheetIdWithIndex(
            wbKey = self.__key,
            wsIndex = index
        )
        return self._deleteWorksheetRsRpc(req)

    def addWorksheetRs(self, ws: Worksheet) -> Result[Worksheet, ErrorReport]:
        req = AddWorksheetRequest(
            wbKey = self.__key,
            worksheet = ws
        )
        outProto: SingleSignalResponseProto = self._wbsv.addWorksheet(request = req.toProtoObj())
        out = SingleSignalResponse.fromProto(outProto)
        if out.isOk():
            ws.workbook = self
            return Ok(ws)
        else:
            return Err(out.errorReport)

    def renameWorksheet(self, oldName: str, newName: str):
        rs = self.renameWorksheetRs(oldName, newName)
        return Results.extractOrRaise(rs)

    def renameWorksheetRs(self, oldName: str, newName: str) -> Result[None, ErrorReport]:
        req = RenameWorksheetRequest(
            wbKey = self.__key,
            oldName = oldName,
            newName = newName
        )
        outProto: SingleSignalResponseProto = self._wbsv.renameWorksheet(request = req.toProtoObj())
        out = SingleSignalResponse.fromProto(outProto)
        return out.toRs()

    @property
    def rootWorkbook(self) -> 'Workbook':
        return self
