from abc import ABC
from pathlib import Path
from typing import Optional, Union, Any

from com.emeraldblast.p6.document_structure.app.errors.AppErrors import AppErrors
from com.emeraldblast.p6.document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from com.emeraldblast.p6.document_structure.communication.SocketProvider import SocketProvider
from com.emeraldblast.p6.document_structure.communication.event_server.EventServer import EventServer
from com.emeraldblast.p6.document_structure.communication.reactor import EventReactorContainer
from com.emeraldblast.p6.document_structure.file.loader.P6FileLoader import P6FileLoader
from com.emeraldblast.p6.document_structure.file.loader.P6FileLoaderErrors import P6FileLoaderErrors
from com.emeraldblast.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.emeraldblast.p6.document_structure.util.for_test.ZZ import writeTestLog
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.util.result.Results import Results
from com.emeraldblast.p6.document_structure.workbook.EventWorkbook import EventWorkbook
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKeyImp import WorkbookKeyImp
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class App(ABC):
    """
    this class represents the state of the app.
    """

    @property
    def zContext(self):
        """zmq context"""
        raise NotImplementedError()

    @property
    def wbContainer(self) -> WorkbookContainer:
        raise NotImplementedError()

    @property
    def _fileSaver(self) -> P6FileSaver:
        raise NotImplementedError()

    @property
    def _fileLoader(self) -> P6FileLoader:
        raise NotImplementedError()

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        raise NotImplementedError()

    def setActiveWorkbook(self, indexOrNameOrKey: Union[int, str, WorkbookKey]):
        """
        Set workbook at indexOrName the active workbook.
        Should raise an exception if the indexOrName is invalid
        """
        raise NotImplementedError()

    def setActiveWorkbookRs(self, indexOrNameOrKey: Union[int, str, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        """
        Set workbook at indexOrName the active workbook.
        :return an Result object if there are error instead of raising an exception
        """
        raise NotImplementedError()

    @property
    def activeSheet(self) -> Optional[Worksheet]:
        """
        :return: the activesheet of the activebook.  The returned worksheet is connected to all the reactors of this app
        """
        raise NotImplementedError()

    def getWorkbookByIndex(self, index: int) -> Workbook:
        """:return workbook at an index. The returned workbook is connected to all the reactors of this app"""
        return self.getWorkbook(index)

    def getWorkbookByName(self, name: str) -> Workbook:
        """:return workbook at a name. The returned workbook is connected to all the reactors of this app"""
        return self.getWorkbook(name)

    def getWorkbookByKey(self, key: WorkbookKey) -> Workbook:
        """:return workbook at a key. The returned workbook is connected to all the reactors of this app"""
        return self.getWorkbook(key)

    def getWorkbook(self, key: Union[str, int, WorkbookKey]) -> Workbook:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is connected to all the reactors of this app
        :raise exception if the workbook is unavailable
        """
        rs: Result[Workbook, ErrorReport] = self.getWorkbookRs(key)
        return Results.extractOrRaise(rs)

    def getWorkbookOrNone(self, key: Union[str, int, WorkbookKey]) -> Workbook|None:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is connected to all the reactors of this app. Return none if the workbook is not available"""
        rs: Result[Workbook, ErrorReport] = self.getWorkbookRs(key)
        return Results.extractOrNone(rs)

    def getWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is connected to all the reactors/notifier of this app"""
        rs = self.getBareWorkbookRs(key)
        if rs.isOk():
            return Ok(self._makeEventWb(rs.value))
        else:
            return rs

    def getBareWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is NOT hooked to any event reactors."""
        wb = self.wbContainer.getWorkbook(key)
        if wb is not None:
            return Ok(wb.rootWorkbook)
        else:
            return Err(AppErrors.WorkbookNotExist(key))

    def hasNoWorkbook(self) -> bool:
        """
        :return: true if this app does not have any workbook
        """
        raise NotImplementedError()

    def createDefaultNewWorkbook(self, name: str | None = None) -> Workbook:
        """
        create a new workbook with an auto generated name, a blank worksheet with auto generated name
        :return a the newly created workbook or raising an exception if there's an error
        """
        createRs: Result[Workbook, ErrorReport] = self.createDefaultNewWorkbookRs(name)
        return Results.extractOrRaise(createRs)

    def createDefaultNewWorkbookRs(self, name: str | None = None) -> Result[Workbook, ErrorReport]:
        """
        create a new workbook with an auto generated name, a blank worksheet with auto generated name
        :return a Result object if there are error instead of raising an exception
        """
        raise NotImplementedError()

    def createNewWorkbook(self, name: Optional[str] = None) -> Workbook:
        """create a new workbook, and add it to this app """
        raise NotImplementedError()

    def createNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        """create a new workbook, and add it to this app 
        :return a Result object if there are error instead of raising an exception
        """
        raise NotImplementedError()

    def hasWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> bool:
        return self.wbContainer.getWorkbook(nameOrIndexOrKey) is not None

    def closeWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]):
        """close a workbook"""
        closeRs = self.closeWorkbookRs(nameOrIndexOrKey)
        if closeRs.isErr():
            raise closeRs.err.toException()

    def closeWorkbookRs(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> Result[WorkbookKey, ErrorReport]:
        """
        close a workbook
        :return a Result object if there are error instead of raising an exception
        """
        wbRs = self.getWorkbookRs(nameOrIndexOrKey)
        if wbRs.isOk():
            self.wbContainer.removeWorkbook(wbRs.value.workbookKey)
            return Ok(wbRs.value.workbookKey)
        else:
            return Err(wbRs.err)

    def forceLoadWorkbook(self, filePath: Union[str, Path]) -> Workbook:
        """force load a workbook from a file path, and add it to this app state"""
        loadRs = self.forceLoadWorkbookRs(filePath)
        if loadRs.isOk():
            wb: Workbook = loadRs.value
            return wb
        else:
            # raise ErrorReports.toException(loadRs.err)
            raise loadRs.err.toException()

    def forceLoadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        """
        force load a workbook from a file path, and add it to this app state, replace whatever workbook with the same key
        :return an Result object if there are error instead of raising an exception
        """
        loadRs: Result[Workbook, ErrorReport] = self._fileLoader.loadRs(Path(filePath))
        if loadRs.isOk():
            self.wbContainer.addWorkbook(loadRs.value)
        return loadRs

    def saveWorkbookAtPath(self, nameOrIndexOrKey: Union[int, str, WorkbookKey], filePath: Union[str, Path]):
        """
         save a workbook at nameOrIndex to a certain filePath, then update the workbook with that new path
        :param nameOrIndexOrKey:
        :param filePath:
        """
        saveRs: Result[Any, ErrorReport] = self.saveWorkbookAtPathRs(nameOrIndexOrKey, filePath)
        Results.extractOrRaise(saveRs)

    def saveWorkbookAtPathRs(self,
                             nameOrIndexOrKey: Union[int, str, WorkbookKey],
                             filePath: Union[str, Path]) -> Result[Workbook|None, ErrorReport]:
        """
         save a workbook at nameOrIndex to a certain filePath, then update the workbook with that new path
        :param nameOrIndexOrKey:
        :param filePath:
        :return: a Result object
        """
        path = Path(filePath)
        getWbRs: Result[Workbook, ErrorReport] = self.getBareWorkbookRs(nameOrIndexOrKey)
        if getWbRs.isOk():
            wb: Workbook = getWbRs.value
            oldKey = wb.workbookKey
            saveResult = self._fileSaver.saveRs(wb, path)
            if saveResult.isOk():
                newKey = WorkbookKeyImp(str(path.name), path)
                if newKey != wb.workbookKey:
                    self.wbContainer.removeWorkbook(oldKey)
                    wb.workbookKey = newKey
                    self.wbContainer.addWorkbook(wb.rootWorkbook)
            return saveResult
        else:
            return getWbRs

    def saveWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]):
        """
        save a workbook at nameOrIndex
        :param nameOrIndexOrKey:
        :return:
        """
        saveRs = self.saveWorkbookRs(nameOrIndexOrKey)
        Results.extractOrRaise(saveRs)

    def saveWorkbookRs(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> Result[Any, ErrorReport]:
        """
        save a workbook at nameOrIndex
        :param nameOrIndexOrKey:
        :return:
        """
        wbRs: Result[Workbook, ErrorReport] = self.getWorkbookRs(nameOrIndexOrKey)
        if wbRs.isOk():
            wb: Workbook = wbRs.value
            saveResult = self.saveWorkbookAtPathRs(nameOrIndexOrKey, wb.workbookKey.filePath)
            return saveResult
        else:
            return wbRs

    def loadWorkbook(self, filePath: Union[str, Path]) -> Workbook:
        """
        load a workbook from a file path, and add it to this app state
        because of the potential difference between file content and loaded content,
        if a workbook is already loaded, attempting loading it will return raise an exception.
        :param filePath:
        :return:
        """
        path = Path(filePath)
        loadRs: Result[Workbook, ErrorReport] = self.loadWorkbookRs(path)
        return Results.extractOrRaise(loadRs)

    def loadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        """
        because of the potential difference between file content and loaded content,
        if a workbook is already loaded, attempting loading it will return an error.
        :param filePath:
        :return:
        """
        path = Path(filePath)
        wbKey = WorkbookKeyImp(str(path.name), path)
        wbRs = self.getWorkbookRs(wbKey)
        alreadyHasThisWorkbook = wbRs.isOk()
        if not alreadyHasThisWorkbook:
            loadResult: Result[Workbook, ErrorReport] = self._fileLoader.loadRs(filePath)
            if loadResult.isOk():
                newWb: Workbook = loadResult.value
                eventNewWb = self._makeEventWb(newWb)
                self.wbContainer.addWorkbook(newWb)
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
        """make WorkbookContainer update-to-date with its elements"""
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

    @property
    def socketProvider(self) -> SocketProvider | None:
        raise NotImplementedError()

    @socketProvider.setter
    def socketProvider(self, socketProvider: SocketProvider | None):
        raise NotImplementedError()

    @property
    def eventReactorContainer(self) -> EventReactorContainer:
        raise NotImplementedError()

    @property
    def eventServer(self)->EventServer:
        raise NotImplementedError()

    def _makeEventWb(self, workbook: Workbook | Optional[Workbook]) -> Optional[EventWorkbook]:
        """wrap a workbook inside an EventWorkbook, give it event callbacks"""
        if workbook is not None:
            if isinstance(workbook, EventWorkbook):
                return workbook
            else:
                return EventWorkbook.create(
                    innerWorkbook = workbook,
                    reactorContainer = self.eventReactorContainer)
        else:
            return None
