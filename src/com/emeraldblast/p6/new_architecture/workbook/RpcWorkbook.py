from pathlib import Path
from typing import Union, Optional, Callable

from com.emeraldblast.p6.document_structure.util.result.Results import Results
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.AddWorksheetRequest import AddWorksheetRequest
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.CreateNewWorksheetRequest import \
    CreateNewWorksheetRequest
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.GetActiveWorksheetResponse import \
    GetActiveWorksheetResponse
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.GetWorksheetResponse import GetWorksheetResponse
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.RenameWorksheetRequest import \
    RenameWorksheetRequest
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.WorksheetWithErrorReportMsg import \
    WorksheetWithErrorReportMsg
from com.emeraldblast.p6.proto.CommonProtos_pb2 import SingleSignalResponseProto

from com.emeraldblast.p6.document_structure.communication.event.data_structure.SingleSignalResponse import \
    SingleSignalResponse
from com.emeraldblast.p6.document_structure.script import SimpleScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.util.CommonError import CommonErrors
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.new_architecture.rpc.RpcErrors import RpcErrors
from com.emeraldblast.p6.new_architecture.rpc.RpcValues import RpcValues
from com.emeraldblast.p6.new_architecture.rpc.StubProvider import RpcServiceProvider
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.GetAllWorksheetsResponse import \
    GetAllWorksheetsResponse
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.IdentifyWorksheetMsg import \
    IdentifyWorksheetMsg
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.SetWbNameRequest import SetWbNameRequest
from com.emeraldblast.p6.proto.service.workbook.CreateNewWorksheetRequestProto_pb2 import CreateNewWorksheetRequestProto
from com.emeraldblast.p6.proto.service.workbook.GetWorksheetResponseProto_pb2 import \
    GetWorksheetResponseProto
from com.emeraldblast.p6.proto.service.workbook.WorksheetWithErrorReportMsgProto_pb2 import \
    WorksheetWithErrorReportMsgProto
from com.emeraldblast.p6.proto.service.workbook.rpc.WorkbookService_pb2_grpc import WorkbookServiceStub


class RpcWorkbook(Workbook):
    _serverDownReport = RpcErrors.RpcServerIsDown \
        .report("Can't get sheet count because rpc server is down.")
    _serverDownException = _serverDownReport.toException()

    def __init__(
            self,
            name: str,
            path: Optional[Path],
            stubProvider: RpcServiceProvider,
    ):
        self.__key = WorkbookKeyImp(name, path)
        self._stubProvider = stubProvider

    def setStubProvider(self, stubProvider: RpcServiceProvider):
        self._stubProvider = stubProvider

    @property
    def _wbsv(self) -> Optional[WorkbookServiceStub]:
        return self._stubProvider.wbService

    ### >> Workbook << ###

    @property
    def worksheets(self) -> list[Worksheet]:
        def f() -> list[Worksheet]:
            outProto = self._wbsv.getAllWorksheets(self.workbookKey.toProtoObj())
            out = GetAllWorksheetsResponse.fromProto(outProto, self)
            return out.worksheets

        return self._onWbsvOk(f)

    @property
    def workbookKey(self) -> WorkbookKey:
        return self.__key

    @workbookKey.setter
    def workbookKey(self, newKey: WorkbookKey):
        self.__key = newKey

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[None, ErrorReport]:
        if isinstance(indexOrName, int):
            return self.setActiveWorksheetByIndexRs(indexOrName)
        elif isinstance(indexOrName, str):
            return self.setActiveWorksheetByNameRs(indexOrName)
        else:
            return Err(CommonErrors.WrongTypeReport("nameOrIndex", "str or int"))

    def setActiveWorksheetByNameRs(self, name: str) -> Result[None, ErrorReport]:
        request = IdentifyWorksheetMsg(
            wbKey = self.workbookKey,
            wsName = name
        )
        return self.setActiveWsRpcRs(request)

    def setActiveWorksheetByIndexRs(self, index: int) -> Result[None, ErrorReport]:
        request = IdentifyWorksheetMsg(
            wbKey = self.workbookKey,
            index = index,
        )
        return self.setActiveWsRpcRs(request)

    def setActiveWsRpcRs(self, request: IdentifyWorksheetMsg) -> Result[None, ErrorReport]:
        def f() -> Result[None, ErrorReport]:
            outProto: SingleSignalResponseProto = self._wbsv.setActiveWorksheet(
                request = request)
            out = SingleSignalResponse.fromProto(outProto)
            if out.isError():
                return Err(out.errorReport)
            else:
                return Ok(None)

        return self._onWbsvOkRs(f)

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        def f() -> Optional[Worksheet]:
            wbsv = self._wbsv
            outProto: GetWorksheetResponseProto = wbsv.getActiveWorksheet(self.workbookKey.toProtoObj())
            out = GetActiveWorksheetResponse.fromProto(outProto, self)
            if out.worksheet:
                return out.worksheet
            else:
                return None

        return self._onWbsvOk(f)

    def isEmpty(self) -> bool:
        return self.sheetCount == 0

    def _onWbsvOkRs(self, f):
        wbsv = self._wbsv
        if wbsv is not None:
            return f()
        else:
            return RpcWorkbook._serverDownReport

    def _onWbsvOk(self, f):
        wbsv = self._wbsv
        if wbsv is not None:
            return f()
        else:
            raise RpcWorkbook._serverDownException

    def _makeGetWsRpcRequestRs(self, request: IdentifyWorksheetMsg) -> Result[Worksheet, ErrorReport]:
        def repStr(index, name) -> str:
            if name:
                return f"Worksheet \"{name}\" does not exist"
            if index:
                return f"Worksheet at index \"{index}\" does not exist"
            else:
                raise CommonErrors.WrongTypeReport("nameOrIndex", "str or int").toException()

        def f():
            outProto: GetWorksheetResponseProto = self._wbsv.getWorksheet(request = request.toProtoObj())
            out = GetWorksheetResponse.fromProto(outProto)
            if out.worksheet:
                return Ok(out.worksheet)
            else:
                return Err(WorkbookErrors.WorksheetNotExistReport.report(repStr(request.index, request.wsName)))

        return self._onWbsvOkRs(f)

    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        req = IdentifyWorksheetMsg(
            wbKey = self.workbookKey,
            wsName = name
        )
        return self._makeGetWsRpcRequestRs(req)

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        req = IdentifyWorksheetMsg(
            wbKey = self.workbookKey,
            index = index
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
                request = self.workbookKey.toProtoObj()
            )
            return out.value
        else:
            raise RpcWorkbook._serverDownException

    @property
    def path(self) -> Path:
        return self.workbookKey.filePath

    @path.setter
    def path(self, newPath: Path):
        self.workbookKey = WorkbookKeys.fromNameAndPath(self.name, newPath)

    @property
    def name(self) -> str:
        return self.workbookKey.fileName

    @name.setter
    def name(self, newName: str):
        if self._wbsv is not None:
            if newName == self.name:
                return
            else:
                outProto = self._wbsv.setWbName(
                    request = SetWbNameRequest(
                        wbKey = self.__key,
                        newName = newName
                    ).toProtoObj()
                )
                out: SingleSignalResponse = SingleSignalResponse.fromProto(outProto)
                err = out.errorReport
                if err is not None:
                    raise err.toException()
                else:
                    self.workbookKey = WorkbookKeys.fromNameAndPath(newName, self.workbookKey.filePath)
        else:
            raise RpcWorkbook._serverDownException

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        def f() -> Result[Worksheet, ErrorReport]:
            req = CreateNewWorksheetRequest(
                wbKey = self.__key,
                newWorksheetName = newSheetName
            ).toProtoObj()
            outProto: WorksheetWithErrorReportMsgProto = self._wbsv.createNewWorksheet(request = req)
            out = WorksheetWithErrorReportMsg.fromProto(outProto, self)
            if out.isErr():
                return Err(out.errorReport)
            else:
                return Ok(out.worksheet)

        return self._onWbsvOkRs(f)

    def _deleteWorksheetRsRpc(self, request: IdentifyWorksheetMsg) -> Result[None, ErrorReport]:
        def f() -> Result[None, ErrorReport]:
            req = request.toProtoObj()
            outProto: SingleSignalResponseProto = self._wbsv.deleteWorksheet(request = req)
            out = SingleSignalResponse.fromProto(outProto)
            return out.toRs()

        return self._onWbsvOkRs(f)

    def deleteWorksheetByNameRs(self, sheetName: str) -> Result[None, ErrorReport]:
        req = IdentifyWorksheetMsg(
            wbKey = self.__key,
            wsName = sheetName
        )
        return self._deleteWorksheetRsRpc(req)

    def deleteWorksheetByIndexRs(self, index: int) -> Result[None, ErrorReport]:
        req = IdentifyWorksheetMsg(
            wbKey = self.__key,
            index = index
        )
        return self._deleteWorksheetRsRpc(req)

    def addWorksheetRs(self, ws: Worksheet) -> Result[None, ErrorReport]:
        def f() -> Result[None, ErrorReport]:
            req = AddWorksheetRequest(
                wbKey = self.__key,
                worksheet = ws
            )
            outProto: SingleSignalResponseProto = self._wbsv.addWorksheet(request = req.toProtoObj())
            out = SingleSignalResponse.fromProto(outProto)
            return out.toRs()

        return self._onWbsvOkRs(f)

    def renameWorksheetName(self, oldName: str, newName: str):
        rs = self.renameWorksheetNameRs(oldName, newName)
        return Results.extractOrRaise(rs)

    def renameWorksheetNameRs(self, oldName: str, newName: str) -> Result[None, ErrorReport]:
        def f() -> Result[None, ErrorReport]:
            req = RenameWorksheetRequest(
                wbKey = self.__key,
                oldName = oldName,
                newName = newName
            )
            outProto: SingleSignalResponseProto = self._wbsv.renameWorksheet(request = req.toProtoObj())
            out = SingleSignalResponse.fromProto(outProto)
            return out.toRs()
        return self._onWbsvOkRs(f)

    @property
    def rootWorkbook(self) -> 'Workbook':
        return self
