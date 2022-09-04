from pathlib import Path
from typing import Callable, Optional, Union

from com.qxdzbc.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp

from com.qxdzbc.p6.document_structure.app.App import App
from com.qxdzbc.p6.document_structure.app.AppWrapper import AppWrapper
from com.qxdzbc.p6.document_structure.communication.event.P6Events import P6Events
from com.qxdzbc.p6.document_structure.communication.event.data_structure.app_event.CloseWorkbookResponse import \
    CloseWorkbookResponse
from com.qxdzbc.p6.document_structure.communication.event.data_structure.app_event.CreateNewWorkbookResponse import \
    CreateNewWorkbookResponse
from com.qxdzbc.p6.document_structure.communication.event.data_structure.app_event.LoadWorkbookResponse import \
    LoadWorkbookResponse
from com.qxdzbc.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookResponse import \
    SaveWorkbookResponse
from com.qxdzbc.p6.document_structure.communication.notifier.eventData.EventData import EventData
from com.qxdzbc.p6.document_structure.communication.reactor.EventReactorContainer import EventReactorContainer
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class EventApp(AppWrapper):

    def __init__(self, innerApp: App, onEvent:Callable[[EventData],None] = None):
        super().__init__(innerApp)
        self.onEvent = onEvent

    @staticmethod
    def create(innerApp:App, reactorContainer: EventReactorContainer)->'EventApp':
        def onEvent(ed:EventData):
            reactorContainer.triggerReactorsFor(ed.event,ed)
        return EventApp(innerApp,onEvent)

    def createDefaultNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        rs = self.rootApp.createDefaultNewWorkbookRs(name)
        self.__emitCreateNeWbEvent(rs)
        return rs

    def createNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
        rs = self.rootApp.createNewWorkbookRs(name)
        self.__emitCreateNeWbEvent(rs)
        return rs

    def __emitCreateNeWbEvent(self,rs:Result[Workbook, ErrorReport]):
        response = CreateNewWorkbookResponse(isError = rs.isErr(), windowId = None)
        if rs.isOk():
            response.workbook = rs.value.rootWorkbook
        if rs.isErr():
            response.errorReport = rs.err
        eventData = EventData(
            event=P6Events.App.CreateNewWorkbook.event,
            data=response)
        self.onEvent(eventData)

    def closeWorkbookRs(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]) -> Result[WorkbookKey, ErrorReport]:
        rs = self.rootApp.closeWorkbookRs(nameOrIndexOrKey)
        if rs.isOk():
            response = CloseWorkbookResponse.fromRs(rs,windowId = None)
            event = P6EventTableImp.i().getEventFor(response)
            self.onEvent(EventData(
                event=event,
                data = response
            ))
        return rs

    def saveWorkbookAtPathRs(
            self,
            nameOrIndexOrKey: Union[int, str, WorkbookKey],
            filePath: str | Path) -> Result[Workbook , ErrorReport]:

        rs = self.rootApp.saveWorkbookAtPathRs(nameOrIndexOrKey, filePath)
        response = SaveWorkbookResponse(
            path = str(Path(filePath).absolute()),
            isError = rs.isErr(),
        )
        if rs.isOk():
            wbKey = rs.value.workbookKey
            response.workbookKey = wbKey
        else:
            response.errorReport = rs.err
        eventData = EventData(
            event = P6Events.App.SaveWorkbook.event,
            data = response
        )
        self.onEvent(eventData)
        return rs

    def loadWorkbookRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        rs = self.rootApp.loadWorkbookRs(filePath)
        response = LoadWorkbookResponse(
            windowId = None,
            isError = rs.isErr(),
        )
        if rs.isOk():
            response.workbook = rs.value
        else:
            response.errorReport = rs.err
        eventData = EventData(
            event = P6Events.App.LoadWorkbook.event,
            data = response
        )
        self.onEvent(eventData)
        return rs