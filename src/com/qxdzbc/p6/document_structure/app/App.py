from abc import ABC
from pathlib import Path
from typing import Optional, Union, Any

from com.qxdzbc.p6.document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from com.qxdzbc.p6.document_structure.communication.SocketProvider import SocketProvider
from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.qxdzbc.p6.document_structure.communication.event_server.EventServer import EventServer
from com.qxdzbc.p6.document_structure.communication.reactor import EventReactorContainer
from com.qxdzbc.p6.document_structure.file.loader.P6FileLoader import P6FileLoader
from com.qxdzbc.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.qxdzbc.p6.document_structure.range.Range import Range
from com.qxdzbc.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.qxdzbc.p6.document_structure.script.ScriptContainer import ScriptContainer
from com.qxdzbc.p6.document_structure.script.ScriptEntry import ScriptEntry
from com.qxdzbc.p6.document_structure.script.ScriptEntryKey import ScriptEntryKey
from com.qxdzbc.p6.document_structure.script.SimpleScriptEntry import SimpleScriptEntry
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.EventWorkbook import EventWorkbook
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet


class App(ABC):
    """
    this class represents the state of the app.
    """

    def addScript(self, name:str, script:str):
        raise NotImplementedError()

    def getScript(self, name:str) -> Optional[str]:
        raise NotImplementedError()

    def removeScript(self, name:str):
        raise NotImplementedError()

    def removeAllScript(self):
        raise NotImplementedError()

    def addAllScripts(self, scripts:list[SimpleScriptEntry]):
        raise NotImplementedError()

    @property
    def allScripts(self)->list[SimpleScriptEntry]:
        raise NotImplementedError()

    @property
    def allAsScriptEntry(self) -> list[ScriptEntry]:
        raise NotImplementedError()

    @property
    def scriptContainer(self) -> ScriptContainer:
        raise NotImplementedError()

    def getRangeRs(self, rangeId: RangeId) -> Result[Range, ErrorReport]:
        raise NotImplementedError()

    def getWorksheetRs(self, workbookKey: WorkbookKey, worksheetName: str) -> Result[Worksheet, ErrorReport]:
        raise NotImplementedError()

    @property
    def rootApp(self) -> 'App':
        raise NotImplementedError()

    @property
    def zContext(self):
        """:return zmq context"""
        raise NotImplementedError()

    @property
    def wbContainer(self) -> WorkbookContainer:
        raise NotImplementedError()

    @property
    def fileSaver(self) -> P6FileSaver:
        raise NotImplementedError()

    @property
    def fileLoader(self) -> P6FileLoader:
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
        raise NotImplementedError()

    def getWorkbookByName(self, name: str) -> Workbook:
        """:return workbook at a name. The returned workbook is connected to all the reactors of this app"""
        raise NotImplementedError()

    def getWorkbookByKey(self, key: WorkbookKey) -> Workbook:
        """:return workbook at a key. The returned workbook is connected to all the reactors of this app"""
        raise NotImplementedError()

    def getWorkbook(self, key: Union[str, int, WorkbookKey]) -> Workbook:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is connected to all the reactors of this app
        :raise exception if the workbook is unavailable
        """
        raise NotImplementedError()

    def getWorkbookOrNone(self, key: Union[str, int, WorkbookKey]) -> Optional[Workbook]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is connected to all the reactors of this app. Return none if the workbook is not available"""
        raise NotImplementedError()

    def getWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is connected to all the reactors/notifier of this app"""
        raise NotImplementedError()

    def getBareWorkbookRs(self, key: Union[str, int, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey. The returned workbook is NOT hooked to any event reactors."""
        raise NotImplementedError()

    def hasNoWorkbook(self) -> bool:
        """
        :return: true if this app does not have any workbook
        """
        raise NotImplementedError()

    def createDefaultNewWorkbook(self, name: Optional[str] = None) -> Workbook:
        """
        create a new workbook with an auto generated name, a blank worksheet with auto generated name
        :return a the newly created workbook or raising an exception if there's an error
        """
        raise NotImplementedError()

    def createDefaultNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
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
        raise NotImplementedError()

    def closeWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]):
        """close a workbook"""
        raise NotImplementedError()

    def closeWorkbookRs(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> Result[WorkbookKey, ErrorReport]:
        """
        close a workbook
        :return a Result object if there are error instead of raising an exception
        """
        raise NotImplementedError()

    def forceLoadWorkbook(self, filePath: Union[str, Path]) -> Workbook:
        """force load a workbook from a file path, and add it to this app state"""
        raise NotImplementedError()

    def forceLoadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        """
        force load a workbook from a file path, and add it to this app state, replace whatever workbook with the same key
        :return an Result object if there are error instead of raising an exception
        """
        raise NotImplementedError()

    def saveWorkbookAtPath(self, nameOrIndexOrKey: Union[int, str, WorkbookKey], filePath: Union[str, Path]):
        """
         save a workbook at nameOrIndex to a certain filePath, then update the workbook with that new path
        :param nameOrIndexOrKey:
        :param filePath:
        """
        raise NotImplementedError()

    def saveWorkbookAtPathRs(self,
                             nameOrIndexOrKey: Union[int, str, WorkbookKey],
                             filePath: str | Path) -> Result[Workbook, ErrorReport]:
        """
         save a workbook at nameOrIndex to a certain filePath, then update the workbook with that new path
        :param nameOrIndexOrKey:
        :param filePath:
        :return: a Result object
        """
        raise NotImplementedError()

    def saveWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]):
        """
        save a workbook at nameOrIndex
        :param nameOrIndexOrKey:
        :return:
        """
        raise NotImplementedError()

    def saveWorkbookRs(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> Result[Any, ErrorReport]:
        """
        save a workbook at nameOrIndex
        :param nameOrIndexOrKey:
        :return:
        """
        raise NotImplementedError()

    def loadWorkbook(self, filePath: Union[str, Path]) -> Workbook:
        """
        load a workbook from a file path, and add it to this app state
        because of the potential difference between file content and loaded content,
        if a workbook is already loaded, attempting loading it will return raise an exception.
        :param filePath:
        :return:
        """
        raise NotImplementedError()

    def loadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        """
        Load a file using the default loader
        :param filePath:
        """

        raise NotImplementedError()

    def refreshContainer(self):
        """make WorkbookContainer update-to-date with its elements"""
        raise NotImplementedError()

    def listWorkbook(self):
        raise NotImplementedError()

    @property
    def socketProvider(self) -> SocketProvider | None:
        raise NotImplementedError()

    @socketProvider.setter
    def socketProvider(self, socketProvider: SocketProvider | None):
        raise NotImplementedError()

    @property
    def eventNotifierContainer(self) -> EventReactorContainer:
        raise NotImplementedError()

    @property
    def eventServer(self) -> EventServer:
        raise NotImplementedError()

    def _makeEventWb(self, workbook: Workbook | Optional[Workbook]) -> Optional[EventWorkbook]:
        """wrap a workbook inside an EventWorkbook, give it event callbacks"""
        raise NotImplementedError()
