from abc import ABC
from pathlib import Path
from typing import Optional, Union, Any, Callable

from bicp_document_structure.app.errors.AppErrors import AppErrors
from bicp_document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.reactor.EventReactorContainer import EventReactorContainer
from bicp_document_structure.file.loader.P6FileLoader import P6FileLoader
from bicp_document_structure.file.loader.P6FileLoaderErrors import P6FileLoaderErrors
from bicp_document_structure.file.saver.P6FileSaver import P6FileSaver
from bicp_document_structure.message.SocketProvider import SocketProvider
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.report.error.ErrorReports import ErrorReports
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.util.result.Results import Results
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.WorkbookKeyImp import WorkbookKeyImp
from bicp_document_structure.worksheet.Worksheet import Worksheet


class App(ABC):
    """
    this class represents the state of the app.
    """

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

    def setActiveWorkbookRs(self, indexOrNameOrKey: Union[int, str, WorkbookKey]) -> Result:
        """
        Set workbook at indexOrName the active workbook.
        :return an Result object if there are error instead of raising an exception
        """
        raise NotImplementedError()

    @property
    def activeSheet(self) -> Optional[Worksheet]:
        raise NotImplementedError()

    def getWorkbookByIndex(self, index: int) -> Optional[Workbook]:
        """:return workbook at an index"""
        return self.wbContainer.getWorkbookByIndex(index)

    def getWorkbookByName(self, name: str) -> Optional[Workbook]:
        """:return workbook at a name"""
        return self.wbContainer.getWorkbookByName(name)

    def getWorkbookByKey(self, key: WorkbookKey) -> Optional[Workbook]:
        """:return workbook at a key"""
        return self.wbContainer.getWorkbookByKey(key)

    def getWorkbook(self, key: Union[str, int, WorkbookKey]) -> Optional[Workbook]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey"""
        return self.wbContainer.getWorkbook(key)

    def getWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey"""
        wb = self.getWorkbook(key)
        if wb is not None:
            return Ok(wb)
        else:
            return Err(
                ErrorReport(
                    header = AppErrors.WorkbookNotExist.header,
                    data = AppErrors.WorkbookNotExist.Data(key),
                )
            )

    def hasNoWorkbook(self) -> bool:
        """
        :return: true if this app does not have any workbook
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
            raise ErrorReports.toException(closeRs.err)

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
            raise ErrorReports.toException(loadRs.err)

    def forceLoadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        """
        force load a workbook from a file path, and add it to this app state, replace whatever workbook with the same key
        :return an Result object if there are error instead of raising an exception
        """
        loadRs: Result[Workbook, ErrorReport] = self._fileLoader.load(Path(filePath))
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
                             filePath: Union[str, Path]) -> Result[Any, ErrorReport]:
        """
         save a workbook at nameOrIndex to a certain filePath, then update the workbook with that new path
        :param nameOrIndexOrKey:
        :param filePath:
        :return: a Result object
        """
        path = Path(filePath)
        getWbRs: Result[Workbook, ErrorReport] = self.getWorkbookRs(nameOrIndexOrKey)
        if getWbRs.isOk():
            wb: Workbook = getWbRs.value
            saveResult = self._fileSaver.save(wb, path)
            if saveResult.isOk():
                newKey = WorkbookKeyImp(wb.workbookKey.fileName, path)
                if newKey != wb.workbookKey:
                    getWbRs.workbookKey = newKey
                    self.wbContainer.addWorkbook(wb)
                    self.refreshContainer()
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
        wbKey = WorkbookKeyImp(path.name, path)
        wb = self.getWorkbook(wbKey)
        alreadyHasThisWorkbook = wb is not None
        if not alreadyHasThisWorkbook:
            loadResult: Result = self._fileLoader.load(filePath, self._getOnCellChange())
            if loadResult.isOk():
                newWb: Workbook = loadResult.value
                # newWb.setOnCellChange(self._getOnCellChange())
                self.wbContainer.addWorkbook(newWb)
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
            rt += "{num}. {wbName}\n".format(
                num = str(i),
                wbName = book.name
            )
        if not rt:
            rt = "No workbook"
        print(rt)

    def _getOnCellChange(self) -> Callable[[Workbook, Worksheet, Cell, P6Event], None]:
        raise NotImplementedError()

    @property
    def socketProvider(self) -> SocketProvider | None:
        raise NotImplementedError

    @socketProvider.setter
    def socketProvider(self, socketProvider: SocketProvider | None):
        raise NotImplementedError
    @property
    def eventReactorContainer(self)->EventReactorContainer:
        raise NotImplementedError