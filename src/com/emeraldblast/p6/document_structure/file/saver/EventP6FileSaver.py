from pathlib import Path
from typing import Union, Callable

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookResponse import \
    SaveWorkbookResponse
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.AppEventData import EventData
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactorContainer import EventReactorContainer
from com.emeraldblast.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class EventP6FileSaver(P6FileSaver):

    def __init__(self,saver,onSave:Callable[[EventData],None]):
        self.saver = saver
        self.onSave = onSave

    @staticmethod
    def create(saver:P6FileSaver,eventNotifierContainer:EventReactorContainer)->'EventP6FileSaver':
        def notify(data:EventData):
            eventNotifierContainer.triggerReactorsFor(data.event, data)
        return EventP6FileSaver(saver,notify)

    def saveRs(self, workbook: Workbook, filePath: Union[str, Path]) -> Result[None, ErrorReport]:
        rs = self.saver.saveRs(workbook,filePath)
        wbKey = workbook.workbookKey
        errReport = None
        if rs.isErr():
            errReport = rs.err

        response = SaveWorkbookResponse(
            path = str(Path(filePath).absolute()),
            isError = rs.isErr(),
        )

        response.errorReport = errReport
        response.workbookKey = wbKey

        eventData = EventData(
            event = P6Events.App.SaveWorkbook.event,
            data = response
        )
        self.onSave(eventData)

        return rs
