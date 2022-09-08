from typing import Optional, Union

from com.qxdzbc.p6.document_structure.file.loader.P6FileLoader import P6FileLoader
from com.qxdzbc.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.qxdzbc.p6.document_structure.script.ScriptContainer import ScriptContainer

from com.qxdzbc.p6.document_structure.app.App import App
from com.qxdzbc.p6.document_structure.app.BaseApp import BaseApp
from com.qxdzbc.p6.document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.new_architecture.communication import EventReactorContainer
from com.qxdzbc.p6.new_architecture.communication import EventServer
from com.qxdzbc.p6.new_architecture.communication import SocketProvider


class AppWrapper(BaseApp):
    """
    a wrapper for app class
    """

    @property
    def scriptContainer(self) -> ScriptContainer:
        return self.rootApp.scriptContainer

    def __init__(self, innerApp: App):
        self.innerApp = innerApp

    @property
    def rootApp(self) -> 'App':
        return self.innerApp

    @property
    def zContext(self):
        return self.rootApp.zContext

    @property
    def wbContainer(self) -> WorkbookContainer:
        return self.rootApp.wbContainer

    @property
    def fileSaver(self) -> P6FileSaver:
        return self.rootApp.fileSaver

    @property
    def fileLoader(self) -> P6FileLoader:
        return self.rootApp.fileLoader

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        return self.rootApp.activeWorkbook

    def setActiveWorkbookRs(self, indexOrNameOrKey: Union[int, str, WorkbookKey]) -> Result[Workbook, ErrorReport]:
        return self.rootApp.setActiveWorkbookRs(indexOrNameOrKey)

    @property
    def activeSheet(self) -> Optional[Worksheet]:
        return self.rootApp.activeSheet

    def hasNoWorkbook(self) -> bool:
        return self.rootApp.hasNoWorkbook()

    def createDefaultNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        return self.rootApp.createDefaultNewWorkbookRs(name)

    def createNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        return self.rootApp.createNewWorkbookRs(name)

    @property
    def socketProvider(self) -> SocketProvider | None:
        return self.rootApp.socketProvider

    @property
    def eventNotifierContainer(self) -> EventReactorContainer:
        return self.rootApp.eventNotifierContainer

    #
    @property
    def eventServer(self) -> EventServer:
        return self.rootApp.eventServer
