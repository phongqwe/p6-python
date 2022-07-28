from pathlib import Path
from typing import Union, Optional

from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.GetActiveWorksheetResponse import \
    GetActiveWorksheetResponse
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
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.SetActiveWorksheetRequest import \
    SetActiveWorksheetRequest
from com.emeraldblast.p6.new_architecture.rpc.data_structure.workbook.SetWbNameRequest import SetWbNameRequest
from com.emeraldblast.p6.proto.service.workbook.GetActiveWorksheetResponseProto_pb2 import \
    GetActiveWorksheetResponseProto
from com.emeraldblast.p6.proto.service.workbook.WorkbookService_pb2_grpc import WorkbookServiceStub


class RpcWorkbook(Workbook):
    _serverDownException = RpcErrors.RpcServerIsDown.report(
        "Can't get sheet count because rpc server is down.").toException()

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
        if self._wbsv is not None:
            outProto = self._wbsv.getAllWorksheets(self.workbookKey.toProtoObj())
            out = GetAllWorksheetsResponse.fromProto(outProto, self)
            return out.worksheets
        else:
            raise RpcWorkbook._serverDownException

    @property
    def workbookKey(self) -> WorkbookKey:
        return self.__key

    @workbookKey.setter
    def workbookKey(self, newKey: WorkbookKey):
        self.__key = newKey

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[None, ErrorReport]:
        if isinstance(indexOrName,int):
            return self.setActiveWorksheetByIndexRs(indexOrName)
        else:
            return self.setActiveWorksheetByNameRs(indexOrName)

    def setActiveWorksheetByNameRs(self, name: str) -> Result[None, ErrorReport]:
        request = SetActiveWorksheetRequest(
            wbKey = self.workbookKey,
            wsName = name
        )
        return self.setActiveWsRpcRs(request)


    def setActiveWorksheetByIndexRs(self, index: int) -> Result[None, ErrorReport]:
        request = SetActiveWorksheetRequest(
            wbKey = self.workbookKey,
            index = index,
        )
        return self.setActiveWsRpcRs(request)

    def setActiveWsRpcRs(self,request:SetActiveWorksheetRequest)->Result[None, ErrorReport]:
        if self._wbsv is not None:
            outProto: SingleSignalResponseProto = self._wbsv.setActiveWorksheetRs(
                request = request)
            out = SingleSignalResponse.fromProto(outProto)
            if out.isError():
                return Err(out.errorReport)
            else:
                return Ok(None)
        else:
            raise RpcWorkbook._serverDownException

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        wbsv = self._wbsv
        if wbsv is not None:
            outProto:GetActiveWorksheetResponseProto = wbsv.getActiveWorksheet(self.workbookKey.toProtoObj())
            out = GetActiveWorksheetResponse.fromProto(outProto,self)
            if out.worksheet:
                return out.worksheet
            else:
                return None
        else:
            raise RpcWorkbook._serverDownException

    def isEmpty(self) -> bool:
        # TODO add rpc call
        pass

    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        # TODO add rpc call
        pass

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        # TODO add rpc call
        pass

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
        # TODO add rpc call
        pass

    def deleteWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        # TODO add rpc call
        pass

    def deleteWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        # TODO add rpc call
        pass

    def addWorksheetRs(self, ws: Worksheet) -> Result[None, ErrorReport]:
        # TODO add rpc call
        pass

    def updateSheetName(self, oldName: str, ws: Worksheet):
        # TODO add rpc call
        pass

    @property
    def rootWorkbook(self) -> 'Workbook':
        return self
