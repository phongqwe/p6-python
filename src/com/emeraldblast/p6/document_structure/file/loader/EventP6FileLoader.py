from pathlib import Path
from typing import Union, Callable

from com.emeraldblast.p6.document_structure.communication.event.data_structure.app_event.LoadWorkbookResponse import \
    LoadWorkbookResponse

from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorContainer import EventReactorContainer
from com.emeraldblast.p6.document_structure.file.loader.P6FileLoader import P6FileLoader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class EventP6FileLoader(P6FileLoader):

    def __init__(self, loader: P6FileLoader, onLoad: Callable[[EventData], None]):
        self.loader = loader
        self.onLoad = onLoad

    @staticmethod
    def create(saver: P6FileLoader, eventNotifierContainer: EventReactorContainer) -> 'EventP6FileLoader':
        def notify(data: EventData):
            eventNotifierContainer.triggerReactorsFor(data.event, data)
        return EventP6FileLoader(saver, notify)

    def loadRs(self, filePath: Union[str, Path]) -> Result[Workbook, ErrorReport]:
        rs = self.loader.loadRs(filePath)
        if rs.isOk():
            response = LoadWorkbookResponse(
                isError = rs.isErr(),
                windowId = None,
                errorReport = None,
                workbook = rs.value
            )
        else:
            response = LoadWorkbookResponse(
                isError = rs.isErr(),
                windowId = None,
                errorReport = rs.err,
                workbook = None
            )
        self.onLoad(response.toEventData())
        return rs

    @property
    def rootLoader(self) -> 'P6FileLoader':
        return self.loader
