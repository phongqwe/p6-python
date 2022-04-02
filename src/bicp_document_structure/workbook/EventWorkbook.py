from functools import partial
from typing import Callable, Optional, Union

from bicp_document_structure.communication.event.data.response.CellUpdateCommonResponse import CellUpdateCommonResponse

from bicp_document_structure.communication.proto.CellProtos_pb2 import CellUpdateCommonResponseProto

from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.event.reactor.EventReactorContainer import EventReactorContainer
from bicp_document_structure.communication.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.communication.event.reactor.eventData.RangeEventData import RangeEventData
from bicp_document_structure.communication.event.reactor.eventData.WorkbookEventData import WorkbookEventData
from bicp_document_structure.communication.event.reactor.eventData.WorksheetEventData import WorksheetEventData
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.util.result.Results import Results
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookWrapper import WorkbookWrapper
from bicp_document_structure.worksheet.EventWorksheet import EventWorksheet
from bicp_document_structure.worksheet.OverrideRenameWorksheet import OverrideRenameWorksheet
from bicp_document_structure.worksheet.Worksheet import Worksheet


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

    def getWorksheetByName(self, name: str) -> Worksheet:
        """wrap the result worksheet in event worksheet, so that it can propagate event"""
        sheet = self._innerWorkbook.getWorksheetByName(name)
        return self.__wrapInEventWorksheet(sheet)

    def getWorksheetByIndex(self, index: int) -> Worksheet:
        """wrap the result worksheet in event worksheet, so that it can propagate event"""
        s = self._innerWorkbook.getWorksheetByIndex(index)
        return self.__wrapInEventWorksheet(s)

    def getWorksheet(self, nameOrIndex: Union[str, int]) -> Worksheet:
        """wrap the result worksheet in event worksheet, so that it can propagate event"""
        s = self._innerWorkbook.getWorksheet(nameOrIndex)
        return self.__wrapInEventWorksheet(s)

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

    def getWorksheetByNameOrNone(self, name: str) -> Worksheet | None:
        rs = self.getWorksheetByNameRs(name)
        return Results.extractOrNone(rs)

    def getWorksheetByIndexOrNone(self, index: int) -> Optional[Worksheet]:
        rs = self.getWorksheetByIndexRs(index)
        return Results.extractOrNone(rs)

    def getWorksheetOrNone(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        rs = self.getWorksheetRs(nameOrIndex)
        return Results.extractOrNone(rs)

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

        if rs.isOk():
            newWorksheet = rs.value
            if self.__onWorkbookEvent is not None:
                wbEventData = WorkbookEventData(
                    workbook = self,
                    isError = rs.isErr(),
                    event = P6Events.Workbook.CreateNewWorksheet.event,
                    data = P6Events.Workbook.CreateNewWorksheet.Response(self.workbookKey, name))
                self.__onWorkbookEvent(wbEventData)
            return Ok(self.__wrapInEventWorksheet(newWorksheet))
        else:
            if self.__onWorkbookEvent is not None:
                errReport: ErrorReport = rs.err
                wbEventData = WorkbookEventData(
                    workbook = self,
                    isError = rs.isErr(),
                    event = P6Events.Workbook.CreateNewWorksheet.event,
                    data = P6Events.Workbook.CreateNewWorksheet.Response(self.workbookKey, name, True, errReport))
                self.__onWorkbookEvent(wbEventData)
            return rs

    def reRun(self):
        self._innerWorkbook.reRun()
        if self.__onWorkbookEvent is not None:
            self.__onWorkbookEvent(WorkbookEventData(self._iwb, P6Events.Workbook.ReRun))

    def __wrapInEventWorksheet(self, sheet: Worksheet) -> Worksheet:
        def onRangeEvent(data: RangeEventData):
            data.workbook = self._innerWorkbook
            if self.__onRangeEvent is not None:
                self.__onRangeEvent(data)

        def onCellEvent(eventData: CellEventData):
            eventData.workbook = self._innerWorkbook
            if eventData.event == P6Events.Cell.Update.event:
                eventData.workbook.reRun()
                protoData = CellUpdateCommonResponse(eventData.workbook)
                eventData.data = protoData
            if self.__onCellChange is not None:
                self.__onCellChange(eventData)

        def onSheetEvent(data: WorksheetEventData):
            data.workbook = self._innerWorkbook
            if self.__onWorksheetEvent is not None:
                self.__onWorksheetEvent(data)

        # update rename function
        return EventWorksheet(
            innerWorksheet = OverrideRenameWorksheet(sheet, renameFunction = self.renameWorksheetRs),
            onCellEvent = onCellEvent,
            onWorksheetEvent = onSheetEvent,
            onRangeEvent = onRangeEvent)

    def __partialWithNoneCheck(self, callback):
        if callback is not None:
            return partial(callback, self._innerWorkbook)
        else:
            return None

    def renameWorksheet(self, oldSheetNameOrIndex: str | int, newSheetName: str):
        rs = self.renameWorksheetRs(oldSheetNameOrIndex, newSheetName)
        if rs.isOk():
            return
        else:
            raise rs.err.toException()

    def renameWorksheetRs(self, oldSheetNameOrIndex: str | int, newSheetName: str) -> Result[None, ErrorReport]:
        rs = self._iwb.renameWorksheetRs(oldSheetNameOrIndex, newSheetName)
        event = P6Events.Worksheet.Rename.event
        DataClass = P6Events.Worksheet.Rename.Response
        if rs.isOk():
            oldName = oldSheetNameOrIndex
            index = self.getIndexOfWorksheet(newSheetName)
            eventData: WorkbookEventData[P6Events.Worksheet.Rename.Response] = WorkbookEventData(
                workbook = self,
                event = event,
                isError = False,
                data = DataClass(self.workbookKey, oldName, newSheetName, index, False, None)
            )
            self.__onWorkbookEvent(eventData)
            return Ok(None)
        else:
            eventData: WorkbookEventData = WorkbookEventData(
                workbook = self,
                event = event,
                isError = True,
                data = DataClass(
                    workbookKey = self.workbookKey,
                    oldName = oldSheetNameOrIndex,
                    newName = newSheetName,
                    index = self.getIndexOfWorksheet(oldSheetNameOrIndex),
                    isError = True,
                    errorReport = rs.err)
            )
            self.__onWorkbookEvent(eventData)
            return rs
