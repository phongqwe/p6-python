from abc import ABC
from pathlib import Path
from typing import Optional, Union, Any

from com.qxdzbc.p6.document_structure.file.loader.P6FileLoader import P6FileLoader
from com.qxdzbc.p6.document_structure.file.loader.P6FileLoaderErrors import P6FileLoaderErrors
from com.qxdzbc.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.qxdzbc.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.qxdzbc.p6.document_structure.script.SimpleScriptEntry import SimpleScriptEntry
from com.qxdzbc.p6.document_structure.workbook.EventWorkbook import EventWorkbook

from com.qxdzbc.p6.document_structure.app.App import App
from com.qxdzbc.p6.document_structure.app.errors.AppErrors import AppErrors
from com.qxdzbc.p6.document_structure.range.Range import Range
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.util.result.Results import Results
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.new_architecture.rpc.data_structure.range import RangeId


class BaseApp(App, ABC):
    @property
    def allScripts(self) -> list[SimpleScriptEntry]:
        return self.scriptContainer.allScripts

    def addScript(self, name: str, script: str):
        self.scriptContainer.addScript(name, script)

    def getScript(self, name: str) -> Optional[str]:
        return self.scriptContainer.getScript(name)

    def removeScript(self, name: str):
        self.scriptContainer.removeScript(name)

    def removeAllScript(self):
        self.scriptContainer.removeAll()

    def addAllScripts(self, scripts: list[SimpleScriptEntry]):
        self.scriptContainer.addAllScripts(scripts)

    @property
    def allAsScriptEntry(self) -> list[ScriptEntry]:
        return self.scriptContainer.allAsScriptEntry(None)

    def getRangeRs(self, rangeId: RangeId) -> Result[Range, ErrorReport]:
        getWbRs = self.getBareWorkbookRs(rangeId.workbookKey)
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

    def createDefaultNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        newWbRs: Result[Workbook, ErrorReport] = self.createNewWorkbookRs(name)
        if newWbRs.isOk():
            wb = newWbRs.value.rootWorkbook
            wb.createNewWorksheetRs()
        return newWbRs

    def createNewWorkbook(self, name: Optional[str] = None) -> Workbook:
        createRs: Result[Workbook, ErrorReport] = self.createNewWorkbookRs(name)
        return Results.extractOrRaise(createRs)

    def setActiveWorkbook(self, indexOrNameOrKey: Union[int, str, WorkbookKey]):
        setRs = self.setActiveWorkbookRs(indexOrNameOrKey)
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

    def getWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        rs = self.getBareWorkbookRs(key)
        if rs.isOk():
            return Ok(self._makeEventWb(rs.value))
        else:
            return rs

    def getBareWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        wb = self.wbContainer.getWorkbook(key)
        if wb is not None:
            return Ok(wb.rootWorkbook)
        else:
            return Err(AppErrors.WorkbookNotExist.report(key))

    def createDefaultNewWorkbook(self, name: Optional[str] = None) -> Workbook:
        createRs: Result[Workbook, ErrorReport] = self.createDefaultNewWorkbookRs(name)
        return Results.extractOrRaise(createRs)

    def hasWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> bool:
        return self.wbContainer.getWorkbook(nameOrIndexOrKey) is not None

    def closeWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]):
        closeRs = self.closeWorkbookRs(nameOrIndexOrKey)
        if closeRs.isErr():
            raise closeRs.err.toException()

    def closeWorkbookRs(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> Result[WorkbookKey, ErrorReport]:
        wbRs = self.getWorkbookRs(nameOrIndexOrKey)
        if wbRs.isOk():
            self.wbContainer.removeWorkbook(wbRs.value.workbookKey)
            return Ok(wbRs.value.workbookKey)
        else:
            return Err(wbRs.err)

    def forceLoadWorkbook(self, filePath: Union[str, Path]) -> Workbook:
        loadRs = self.forceLoadWorkbookRs(filePath)
        if loadRs.isOk():
            wb: Workbook = loadRs.value
            return wb
        else:
            raise loadRs.err.toException()

    def forceLoadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        loadRs: Result[Workbook, ErrorReport] = self.fileLoader.loadRs(Path(filePath))
        if loadRs.isOk():
            self.wbContainer.addWorkbook(loadRs.value)
        return loadRs

    def saveWorkbookAtPath(self, nameOrIndexOrKey: Union[int, str, WorkbookKey], filePath: Union[str, Path]):
        saveRs: Result[Any, ErrorReport] = self.saveWorkbookAtPathRs(nameOrIndexOrKey, filePath)
        Results.extractOrRaise(saveRs)

    def saveWorkbookAtPathRs(self,
                             nameOrIndexOrKey: Union[int, str, WorkbookKey],
                             filePath: str | Path) -> Result[Workbook , ErrorReport]:
        saver: P6FileSaver = self.fileSaver
        path = Path(filePath)
        getWbRs: Result[Workbook, ErrorReport] = self.getBareWorkbookRs(nameOrIndexOrKey)
        if getWbRs.isOk():
            wb: Workbook = getWbRs.value
            oldKey = wb.workbookKey
            saveResult = saver.saveRs(wb, path)
            if saveResult.isOk():
                newKey = WorkbookKeyImp(str(path.name), path)
                if newKey != wb.workbookKey:
                    self.wbContainer.removeWorkbook(oldKey)
                    wb.workbookKey = newKey
                    self.wbContainer.addWorkbook(wb.rootWorkbook)
                    wb.refreshScript()
                return Ok(wb)
            else:
                return Err(saveResult.err)
        else:
            return getWbRs

    def saveWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]):
        saveRs = self.saveWorkbookRs(nameOrIndexOrKey)
        Results.extractOrRaise(saveRs)

    def saveWorkbookRs(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> Result[Any, ErrorReport]:
        wbRs: Result[Workbook, ErrorReport] = self.getWorkbookRs(nameOrIndexOrKey)
        if wbRs.isOk():
            wb: Workbook = wbRs.value
            saveResult = self.saveWorkbookAtPathRs(nameOrIndexOrKey, wb.workbookKey.filePath)
            return saveResult
        else:
            return wbRs

    def loadWorkbook(self, filePath: Union[str, Path]) -> Workbook:
        path = Path(filePath)
        loadRs: Result[Workbook, ErrorReport] = self.loadWorkbookRs(path)
        return Results.extractOrRaise(loadRs)

    def loadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        loader: P6FileLoader = self.fileLoader
        path = Path(filePath)
        wbKey = WorkbookKeyImp(str(path.name), path)
        wbRs = self.getWorkbookRs(wbKey)
        alreadyHasThisWorkbook = wbRs.isOk()
        if not alreadyHasThisWorkbook:
            loadResult: Result[Workbook, ErrorReport] = loader.loadRs(filePath)
            if loadResult.isOk():
                newWb: Workbook = loadResult.value
                eventNewWb = self._makeEventWb(newWb)
                self.wbContainer.addWorkbook(newWb)
                # the file may have been move, therefore has different workbook key,
                # must refresh script because the old script contains code for the old workbook key
                newWb.refreshScript()
                return Ok(eventNewWb)
            else:
                return loadResult
        else:
            return Err(
                ErrorReport(
                    header = P6FileLoaderErrors.AlreadyLoad.header,
                    data = P6FileLoaderErrors.AlreadyLoad.Data(path, None)
                )
            )

    def refreshContainer(self):
        bookList = self.wbContainer.books()
        self.wbContainer.clear()
        for book in bookList:
            self.wbContainer.addWorkbook(book)

    def listWorkbook(self):
        rt = ""
        for (i, book) in enumerate(self.wbContainer.books()):
            rt += f"{str(i)}. {book.name}\n"
        if not rt:
            rt = "No workbook"
        print(rt)

    def _makeEventWb(self, workbook: Workbook | Optional[Workbook]) -> Optional[EventWorkbook]:
        """create eventful workbook"""
        if workbook is not None:
            if isinstance(workbook, EventWorkbook):
                return workbook
            else:
                return EventWorkbook.create(
                    innerWorkbook = workbook,
                    reactorContainer = self.eventNotifierContainer)
        else:
            return None
