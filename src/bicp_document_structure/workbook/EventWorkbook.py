from functools import partial
from typing import Callable, Optional, Union

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.P6Events import P6Events
from bicp_document_structure.message.event.reactor.EventReactorContainer import EventReactorContainer
from bicp_document_structure.message.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.message.event.reactor.eventData.RangeEventData import RangeEventData
from bicp_document_structure.message.event.reactor.eventData.WorkbookEventData import WorkbookEventData
from bicp_document_structure.message.event.reactor.eventData.WorksheetEventData import WorksheetEventData
from bicp_document_structure.range.Range import Range
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookWrapper import WorkbookWrapper
from bicp_document_structure.worksheet.EventWorksheet import EventWorksheet
from bicp_document_structure.worksheet.Worksheet import Worksheet


class EventWorkbook(WorkbookWrapper):
    """
    The reason EventReactorContainer is not injected here directly because they can
    """

    def __init__(self, innerWorkbook: Workbook,
                 onCellEvent: Callable[[Workbook, Worksheet, Cell, P6Event], None] = None,
                 onWorksheetEvent: Callable[[WorksheetEventData], None] = None,
                 onRangeEvent: Callable[[Workbook, Worksheet, Range, P6Event], None] = None,
                 onWorkbookEvent: Callable[[WorkbookEventData], None] = None,
                 ):
        super().__init__(innerWorkbook)
        self.__onCellChange: Callable[[Workbook, Worksheet, Cell, P6Event], None] = onCellEvent
        self.__onWorksheetEvent: Callable[[WorksheetEventData], None] = onWorksheetEvent
        self.__onRangeEvent: Callable[[Workbook, Worksheet, Range, P6Event], None] = onRangeEvent
        self.__onWorkbookEvent: Callable[[WorkbookEventData], None] = onWorkbookEvent
        self._iwb = self._innerWorkbook

    @staticmethod
    def create(innerWorkbook: Workbook, reactorContainer: EventReactorContainer) -> 'EventWorkbook':
        def onCell(wb, ws, c, e):
            reactorContainer.triggerReactorsFor(e, CellEventData(wb, ws, c, e))

        def onWorkbook(data: WorkbookEventData):
            reactorContainer.triggerReactorsFor(data.event, data)

        def onWorksheet(data: WorksheetEventData):
            reactorContainer.triggerReactorsFor(data.event, data)

        def onRange(wb, ws, r, e):
            reactorContainer.triggerReactorsFor(e, RangeEventData(wb, ws, r, e))

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

    def getWorksheetByName(self, name: str) -> Optional[Worksheet]:
        """wrap the result worksheet in event worksheet, so that it can propagate event"""
        sheet = self._innerWorkbook.getWorksheetByName(name)
        if sheet is not None:
            return self.__wrapInEventWorksheet(sheet)
        else:
            return sheet

    def getWorksheetByIndex(self, index: int) -> Optional[Worksheet]:
        """wrap the result worksheet in event worksheet, so that it can propagate event"""
        s = self._innerWorkbook.getWorksheetByIndex(index)
        if s is not None:
            return self.__wrapInEventWorksheet(s)
        else:
            return s

    def getWorksheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        """wrap the result worksheet in event worksheet, so that it can propagate event"""
        s = self._innerWorkbook.getWorksheet(nameOrIndex)
        if s is not None:
            return self.__wrapInEventWorksheet(s)
        else:
            return s

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
                    data = P6Events.Workbook.CreateNewWorksheet.Data(self.workbookKey, name))
                self.__onWorkbookEvent(wbEventData)
            return Ok(self.__wrapInEventWorksheet(newWorksheet))
        else:
            if self.__onWorkbookEvent is not None:
                errReport: ErrorReport = rs.err
                wbEventData = WorkbookEventData(
                    workbook = self,
                    isError = rs.isErr(),
                    event = P6Events.Workbook.CreateNewWorksheet.event,
                    data = P6Events.Workbook.CreateNewWorksheet.Data(self.workbookKey, name, True, errReport))
                self.__onWorkbookEvent(wbEventData)
            return rs

    def reRun(self):
        self._innerWorkbook.reRun()
        if self.__onWorkbookEvent is not None:
            self.__onWorkbookEvent(WorkbookEventData(self._iwb, P6Events.Workbook.ReRun))

    def __wrapInEventWorksheet(self, sheet: Worksheet) -> Worksheet:
        onCellEvent = self.__partialWithNoneCheck(self.__onCellChange)
        onSheetEvent = self.__partialWithNoneCheck(self.__onWorksheetEvent)
        onRangeEvent = self.__partialWithNoneCheck(self.__onRangeEvent)
        return EventWorksheet(sheet,
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
        if rs.isOk():
            oldName = oldSheetNameOrIndex
            index = self.getIndexOfWorksheet(newSheetName)
            eventData: WorksheetEventData[P6Events.Worksheet.RenameOk.Data] = WorksheetEventData(
                workbook = self,
                worksheet = self.getWorksheet(newSheetName),
                event = P6Events.Worksheet.RenameOk.event,
                isError = False,
                data = P6Events.Worksheet.RenameOk.Data(self.workbookKey, oldName, newSheetName, index)
            )
            self.__onWorksheetEvent(eventData)
            return Ok(None)
        else:
            eventData: WorksheetEventData = WorksheetEventData(
                workbook = self,
                worksheet = self.getWorksheet(oldSheetNameOrIndex),
                event = P6Events.Worksheet.RenameOk.event,
                isError = True,
                data = P6Events.Worksheet.RenameOk.Data(self.workbookKey, oldSheetNameOrIndex, newSheetName,
                                                        self.getIndexOfWorksheet(oldSheetNameOrIndex))
            )
            self.__onWorksheetEvent(eventData)
            return rs
