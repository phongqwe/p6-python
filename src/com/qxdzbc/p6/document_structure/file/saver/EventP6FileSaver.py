from pathlib import Path
from typing import Union, Callable

from com.qxdzbc.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp

from com.qxdzbc.p6.document_structure.communication.event.P6Events import P6Events
from com.qxdzbc.p6.document_structure.communication.event.data_structure.workbook_event.save_wb.SaveWorkbookResponse import \
    SaveWorkbookResponse
from com.qxdzbc.p6.document_structure.communication.notifier.eventData.EventData import EventData
from com.qxdzbc.p6.document_structure.communication.reactor.EventReactorContainer import EventReactorContainer
from com.qxdzbc.p6.document_structure.file.saver.P6FileSaver import P6FileSaver
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook


class EventP6FileSaver(P6FileSaver):

    @property
    def rootSaver(self) -> 'P6FileSaver':
        return self.saver

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
            event = P6EventTableImp.i().getEventFor(response),
            data = response
        )
        self.onSave(eventData)

        return rs
