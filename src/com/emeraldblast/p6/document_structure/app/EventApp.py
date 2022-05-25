from typing import Callable, Optional

from com.emeraldblast.p6.document_structure.app.App import App
from com.emeraldblast.p6.document_structure.app.AppWrapper import AppWrapper
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorContainer import EventReactorContainer
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
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

    # def createDefaultNewWorkbookRs(self, name: str | None = None) -> Result[Workbook, ErrorReport]:
    #     rt = self.rootApp.createDefaultNewWorkbookRs(name)
    #
    #
    #     return rt
    #
    # def createNewWorkbookRs(self, name: Optional[str] = None) -> Result[Workbook, ErrorReport]:
    #     return super().createNewWorkbookRs(name)




