from typing import Callable, Optional, Union

from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.DeleteWorksheetResponse import \
    DeleteWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.RangeEventData import \
    RangeEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorkbookEventData import \
    WorkbookEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorksheetEventData import \
    WorksheetEventData
from com.emeraldblast.p6.document_structure.communication.reactor import EventReactorContainer
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.WorkbookWrapper import WorkbookWrapper
from com.emeraldblast.p6.document_structure.worksheet.EventWorksheet import EventWorksheet
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class EventWorkbook(WorkbookWrapper):
    """
    The reason EventReactorContainer is not injected here directly because they can
    """

    def __init__(self, innerWorkbook: Workbook,
                 onCellEvent: Callable[[CellEventData], None] = None,
                 onWorksheetEvent: Callable[[WorksheetEventData], None] = None,
                 onRangeEvent: Callable[[RangeEventData], None] = None,
                 onWorkbookEvent: Callable[[WorkbookEventData], None] = None,
                 ):
        super().__init__(innerWorkbook)
        self.__onCellChange: Callable[[CellEventData], None] = onCellEvent
        self.__onWorksheetEvent: Callable[[WorksheetEventData], None] = onWorksheetEvent
        self.__onRangeEvent: Callable[[RangeEventData], None] = onRangeEvent
        self.__onWorkbookEvent: Callable[[WorkbookEventData], None] = onWorkbookEvent
        self._iwb = self._innerWorkbook

    @staticmethod
    def create(innerWorkbook: Workbook, reactorContainer: EventReactorContainer) -> 'EventWorkbook':
        def onCell(data: CellEventData):
            reactorContainer.triggerReactorsFor(data.event, data)

        def onWorkbook(data: WorkbookEventData):
            reactorContainer.triggerReactorsFor(data.event, data)

        def onWorksheet(data: WorksheetEventData):
            reactorContainer.triggerReactorsFor(data.event, data)

        def onRange(data: RangeEventData):
            reactorContainer.triggerReactorsFor(data.event, data)

        return EventWorkbook(
            innerWorkbook = innerWorkbook,
            onCellEvent = onCell,
            onWorksheetEvent = onWorksheet,
            onRangeEvent = onRange,
            onWorkbookEvent = onWorkbook,
        )

    @property
    def worksheets(self) -> list[Worksheet]:
        """wrap the result worksheets in event worksheet, so that they can propagate event"""
        sheets = self._innerWorkbook.worksheets
        rt = list(map(lambda s: self.__wrapInEventWorksheet(s), sheets))
        return rt

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        """wrap the result worksheet in event worksheet, so that it can propagate event"""
        activeSheet = self._innerWorkbook.activeWorksheet
        return self.__wrapInEventWorksheet(activeSheet)

    def __handleWsRs(self, rs: Result[Worksheet, ErrorReport]):
        if rs.isOk():
            return Ok(self.__wrapInEventWorksheet(rs.value))
        else:
            return rs

    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        rs = self._iwb.getWorksheetByNameRs(name)
        return self.__handleWsRs(rs)

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        rs = self._iwb.getWorksheetByIndexRs(index)
        return self.__handleWsRs(rs)

    def getWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        rs = self._iwb.getWorksheetRs(nameOrIndex)
        return self.__handleWsRs(rs)

    def createNewWorksheet(self, newSheetName: Optional[str]) -> Worksheet:
        rs = self.createNewWorksheetRs(newSheetName)
        if rs.isOk():
            return rs.value
        else:
            raise rs.err.toException()

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        rs = self._iwb.createNewWorksheetRs(newSheetName)

        name = str(newSheetName)
        if rs.isOk():
            name = rs.value.name

        wbEventData = WorkbookEventData(
            workbook = self,
            event = P6Events.Workbook.CreateNewWorksheet.event)
        if rs.isOk():
            newWorksheet = rs.value
            if self.__onWorkbookEvent is not None:
                wbEventData.data = P6Events.Workbook.CreateNewWorksheet.Response(self.workbookKey, name)
                self.__onWorkbookEvent(wbEventData)
            return Ok(self.__wrapInEventWorksheet(newWorksheet))
        else:
            if self.__onWorkbookEvent is not None:
                errReport: ErrorReport = rs.err
                wbEventData.data = P6Events.Workbook.CreateNewWorksheet.Response(self.workbookKey, name, True,
                                                                                 errReport)
                self.__onWorkbookEvent(wbEventData)
            return rs

    def reRun(self):
        self._innerWorkbook.reRun()
        if self.__onWorkbookEvent is not None:
            self.__onWorkbookEvent(WorkbookEventData(self._iwb, P6Events.Workbook.ReRun.event))

    def __wrapInEventWorksheet(self, sheet: Worksheet) -> Worksheet:
        def onRangeEvent(data: RangeEventData):
            if self.__onRangeEvent is not None:
                self.__onRangeEvent(data)

        def onCellEvent(eventData: CellEventData):
            if self.__onCellChange is not None:
                self.__onCellChange(eventData)

        def onSheetEvent(data: WorksheetEventData):
            if self.__onWorksheetEvent is not None:
                self.__onWorksheetEvent(data)

        # update rename function
        return EventWorksheet(
            innerWorksheet = sheet,
            onCellEvent = onCellEvent,
            onWorksheetEvent = onSheetEvent,
            onRangeEvent = onRangeEvent)

    def deleteWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        rs = self._iwb.deleteWorksheetByNameRs(sheetName)
        response = DeleteWorksheetResponse(
            workbookKey = self.workbookKey,
            # targetWorksheet = [sheetName],
            isError = rs.isErr()
        )

        eventData = WorkbookEventData(
            workbook = self,
            event = P6Events.Workbook.DeleteWorksheet.event,
            data = response
        )
        if rs.isOk():
            response.targetWorksheet = sheetName

        if rs.isErr():
            response.errorReport = rs.err
        self.__onWorkbookEvent(eventData)
        return rs

    def deleteWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        rs = self._iwb.deleteWorksheetByIndexRs(index)
        response = DeleteWorksheetResponse(
            workbookKey = self.workbookKey,
            isError = rs.isErr()
        )
        eventData = WorkbookEventData(
            workbook = self,
            event = P6Events.Workbook.DeleteWorksheet.event,
            data = response
        )
        if rs.isOk():
            response.targetWorksheet = rs.value.name
        if rs.isErr():
            response.errorReport = rs.err
        self.__onWorkbookEvent(eventData)
        return rs