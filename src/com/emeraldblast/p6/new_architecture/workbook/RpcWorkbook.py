from pathlib import Path
from typing import Union, Optional, Tuple
import google.protobuf.empty_pb2 as empty_pb2

from google.protobuf import wrappers_pb2 as wrappers
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from com.emeraldblast.p6.document_structure.script import SimpleScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.emeraldblast.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.emeraldblast.p6.document_structure.script.ScriptContainerImp import ScriptContainerImp
from com.emeraldblast.p6.document_structure.script.ScriptContainerImp import ScriptContainerImp
from com.emeraldblast.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.emeraldblast.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.emeraldblast.p6.document_structure.util.CommonError import CommonErrors
from com.emeraldblast.p6.document_structure.util.Util import typeCheck
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookErrors import WorkbookErrors
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeys import WorkbookKeys
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp
from com.emeraldblast.p6.new_architecture.rpc.RpcErrors import RpcErrors
from com.emeraldblast.p6.new_architecture.rpc.RpcValues import RpcValues
from com.emeraldblast.p6.new_architecture.rpc.StubProvider import StubProvider
from com.emeraldblast.p6.proto.service.workbook.WorkbookService_pb2_grpc import WorkbookServiceStub



class RpcWorkbook(Workbook):

    def __init__(
            self,
            name: str,
            path: Optional[Path],
            stubProvider: StubProvider,
    ):
        self.__key = WorkbookKeyImp(name, path)
        self._stubProvider = stubProvider

    @property
    def _sv(self) -> Optional[WorkbookServiceStub]:
        return self._stubProvider.wbService

    def removeScriptRs(self, name: str) -> Result[None, ErrorReport]:
        # TODO this is a place holder for future checking
        return Ok(None)

    def addAllScriptsRs(self, scripts: list[SimpleScriptEntry]) -> Result[None, ErrorReport]:
        return Ok(None)

    def overwriteScriptRs(self, name: str, newScript: str) -> Result[None, ErrorReport]:
        return Ok(None)

    def overwriteScript(self, name: str, newScript: str):
        rs = self.overwriteScriptRs(name, newScript)
        rs.getOrRaise()

    def addScriptRs(self, name: str, script: str) -> Result[None, ErrorReport]:
        return Ok(None)

    @property
    def allAsScriptEntry(self) -> list[ScriptEntry]:
        pass

    def getScript(self, name: str) -> Optional[str]:
        pass

    def removeAllScript(self):
        pass

    def addAllScripts(self, scripts: list[SimpleScriptEntry]):
        pass

    @property
    def allScripts(self) -> list[ScriptEntry]:
        pass

    ### >> Workbook << ###

    @property
    def worksheets(self) -> list[Worksheet]:
        # TODO add rpc call
        pass

    @property
    def workbookKey(self) -> WorkbookKey:
        return self.__key

    @workbookKey.setter
    def workbookKey(self, newKey: WorkbookKey):
        self.__key = newKey

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[Worksheet, ErrorReport]:
        # TODO add rpc call
        pass

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        # TODO add rpc call
        pass

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
        if self._sv is not None:
            out:RpcValues.Int64Value = self._sv.sheetCount(request = RpcValues.Empty)
            return out.value
        else:
            raise RpcErrors.RpcServerIsDown.report("Can't get sheet count because rpc server is down.")

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
        # TODO add rpc call
        pass

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
