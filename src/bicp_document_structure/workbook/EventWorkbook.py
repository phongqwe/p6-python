from functools import partial
from typing import Callable, Optional, Union

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.P6Events import P6Events
from bicp_document_structure.range.Range import Range
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookWrapper import WorkbookWrapper
from bicp_document_structure.worksheet.EventWorksheet import EventWorksheet
from bicp_document_structure.worksheet.Worksheet import Worksheet


class EventWorkbook(WorkbookWrapper):
    def __init__(self, innerWorkbook: Workbook,
                 onCellEvent: Callable[[Workbook, Worksheet, Cell, P6Event], None] = None,
                 onWorksheetEvent: Callable[[Workbook, Worksheet, P6Event], None] = None,
                 onRangeEvent: Callable[[Workbook, Worksheet, Range, P6Event], None] = None,
                 onWorkbookEvent: Callable[[Workbook, P6Event], None] = None,
                 ):
        super().__init__(innerWorkbook)
        self.__onCellChange: Callable[[Workbook, Worksheet, Cell, P6Event], None] = onCellEvent
        self.__onWorksheetEvent: Callable[[Workbook, Worksheet, P6Event], None] = onWorksheetEvent
        self.__onRangeEvent: Callable[[Workbook, Worksheet, Range, P6Event], None] = onRangeEvent
        self.__onWorkbookEvent: Callable[[Workbook, P6Event], None] = onWorkbookEvent

    @property
    def worksheets(self) -> list[Worksheet]:
        sheets = self._innerWorkbook.worksheets
        rt = list(map(lambda s: self.__wrapInEventWorksheet(s), sheets))
        return rt

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        activeSheet = self._innerWorkbook.activeWorksheet
        return self.__wrapInEventWorksheet(activeSheet)

    def getWorksheetByName(self, name: str) -> Optional[Worksheet]:
        s = self._innerWorkbook.getWorksheetByName(name)
        if s is not None:
            return self.__wrapInEventWorksheet(s)
        else:
            return s

    def getWorksheetByIndex(self, index: int) -> Optional[Worksheet]:
        s = self._innerWorkbook.getWorksheetByIndex(index)
        if s is not None:
            return self.__wrapInEventWorksheet(s)
        else:
            return s

    def getWorksheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        s = self._innerWorkbook.getWorksheet(nameOrIndex)
        if s is not None:
            return self.__wrapInEventWorksheet(s)
        else:
            return s

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        s = self._innerWorkbook.createNewWorksheetRs(newSheetName)
        if s.isOk():
            return Ok(self.__wrapInEventWorksheet(s.value))
        else:
            return s

    def reRun(self):
        self._innerWorkbook.reRun()
        if self.__onWorkbookEvent is not None:
            self.__onWorkbookEvent(self._innerWorkbook, P6Events.Workbook.ReRun)

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