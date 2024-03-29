from abc import ABC
from pathlib import Path
from typing import Optional, Union, Any

from com.qxdzbc.p6.app.App import App
from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.util.result.Results import Results
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.range.rpc_data_structure.RangeId import RangeId


class BaseApp(App, ABC):
    # @property
    # def allScripts(self) -> list[SimpleScriptEntry]:
    #     return self.scriptContainer.allScripts
    #
    # def addScript(self, name: str, script: str):
    #     self.scriptContainer.addScript(name, script)
    #
    # def getScript(self, name: str) -> Optional[str]:
    #     return self.scriptContainer.getScript(name)
    #
    # def removeScript(self, name: str):
    #     self.scriptContainer.removeScript(name)
    #
    # def removeAllScript(self):
    #     self.scriptContainer.removeAll()
    #
    # def addAllScripts(self, scripts: list[SimpleScriptEntry]):
    #     self.scriptContainer.addAllScripts(scripts)
    #
    # @property
    # def allAsScriptEntry(self) -> list[ScriptEntry]:
    #     return self.scriptContainer.allAsScriptEntry(None)

    def getRangeRs(self, rangeId: RangeId) -> Result[Range, ErrorReport]:
        getWbRs = self.getWorkbookRs(rangeId.workbookKey)
        if getWbRs.isOk():
            wb = getWbRs.value
            getWsRs = wb.getWorksheetRs(rangeId.worksheetName)
            if getWsRs.isOk():
                ws = getWsRs.value
                return Ok(ws.range(rangeId.rangeAddress))
            else:
                return Err(getWsRs.err)
        else:
            return Err(getWbRs.err)

    def getWorksheetRs(self,workbookKey:WorkbookKey, worksheetName:str)->Result[Worksheet,ErrorReport]:
        wbRs = self.getWorkbookRs(workbookKey)
        if wbRs.isOk():
            wb = wbRs.value
            wsRs = wb.getWorksheetRs(worksheetName)
            return wsRs
        else:
            return Err(wbRs.err)

    @property
    def rootApp(self) -> 'App':
        return self

    def createNewWorkbook(self, name: Optional[str] = None) -> Workbook:
        createRs: Result[Workbook, ErrorReport] = self.createNewWorkbookRs(name)
        return Results.extractOrRaise(createRs)

    def setActiveWorkbook(self, wbKey: Union[int, str, WorkbookKey]):
        setRs = self.setActiveWorkbookRs(wbKey)
        return Results.extractOrRaise(setRs)

    def getWorkbookByIndex(self, index: int) -> Workbook:
        return self.getWorkbook(index)

    def getWorkbookByName(self, name: str) -> Workbook:
        return self.getWorkbook(name)

    def getWorkbookByKey(self, key: WorkbookKey) -> Workbook:
        return self.getWorkbook(key)

    def getWorkbook(self, key: Union[str, int, WorkbookKey]) -> Workbook:
        rs: Result[Workbook, ErrorReport] = self.getWorkbookRs(key)
        return Results.extractOrRaise(rs)

    def getWorkbookOrNone(self, key: Union[str, int, WorkbookKey]) -> Optional[Workbook]:
        rs: Result[Workbook, ErrorReport] = self.getWorkbookRs(key)
        return Results.extractOrNone(rs)

    def closeWorkbookByWbKey(self, wbKey:WorkbookKey)->WorkbookKey:
        closeRs = self.closeWorkbookByWbKeyRs(wbKey)
        return Results.extractOrRaise(closeRs)

    def saveWorkbookAtPath(self, wbKey:WorkbookKey, filePath: Union[str, Path]):
        saveRs: Result[Any, ErrorReport] = self.saveWorkbookAtPathRs(wbKey, filePath)
        Results.extractOrRaise(saveRs)

    def saveWorkbook(self, wbKey:WorkbookKey):
        saveRs = self.saveWorkbookRs(wbKey)
        Results.extractOrRaise(saveRs)

    def saveWorkbookRs(self, wbKey:WorkbookKey) -> Result[Any, ErrorReport]:
        saveResult = self.saveWorkbookAtPathRs(wbKey, wbKey.filePath)
        return saveResult

    def loadWorkbook(self, filePath: Union[str, Path]) -> Workbook:
        path = Path(filePath)
        loadRs: Result[Workbook, ErrorReport] = self.loadWorkbookRs(path)
        return Results.extractOrRaise(loadRs)

    def printWorkbookSummary(self):
        rt = ""
        for (i, book) in enumerate(self.workbooks):
            rt += f"{str(i)}. {book.name}\n"
        if not rt:
            rt = "No workbook"
        print(rt)

    def closeWorkbook(self, keyOrNameOrIndex: Union[WorkbookKey, str, int]) -> WorkbookKey:
        rs = self.closeWorkbookRs(keyOrNameOrIndex)
        return rs.getOrRaise()