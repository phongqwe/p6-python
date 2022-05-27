from typing import Callable, Optional

from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.CreateNewWorkbookResponse import \
    CreateNewWorkbookResponse

from com.emeraldblast.p6.document_structure.app.App import App
from com.emeraldblast.p6.document_structure.app.AppWrapper import AppWrapper
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorContainer import EventReactorContainer
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class EventApp(AppWrapper):

    def __init__(self, innerApp: App, onEvent:Callable[[EventData],None] = None):
        super().__init__(innerApp)
        self.onEvent = onEvent

    @staticmethod
    def create(innerApp:App, reactorContainer: EventReactorContainer)->'EventApp':
        def onEvent(ed:EventData):
            reactorContainer.triggerReactorsFor(ed.event,ed)
        return EventApp(innerApp,onEvent)

    def createDefaultNewWorkbookRs(self, name: str | None = None) -> Result[Workbook, ErrorReport]:
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
            isError = False,
            data=response.toProtoBytes())
        self.onEvent(eventData)
