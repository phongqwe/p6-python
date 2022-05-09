from typing import Callable

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.WrapperCell import WrapperCell
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.WorkbookUpdateCommonResponse import \
    WorkbookUpdateCommonResponse
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData


class EventCell(WrapperCell):
    """
    A cell wrapper that trigger event reactors at certain events
    """

    def __init__(self,
                 innerCell: Cell,
                 onCellEvent: Callable[[CellEventData], None] = None):
        super().__init__(innerCell)
        self.__onCellEvent = onCellEvent
        self._ic = innerCell

    @WrapperCell.value.setter
    def value(self, newValue):
        self._innerCell.value = newValue
        if self.__onCellEvent is not None:
            if self.workbook is not None:
                self.workbook.reRun()
            protoData = WorkbookUpdateCommonResponse(
                isError=False,
                workbookKey = self.workbook.workbookKey,
                newWorkbook = self.workbook)
            eventData = CellEventData(
                workbook = self.workbook,
                cell = self._ic,
                event = P6Events.Cell.Update.event,
                data = protoData
            )
            self.__onCellEvent(eventData)

    @WrapperCell.script.setter
    def script(self, newScript: str):
        self._innerCell.script = newScript
        if self.__onCellEvent is not None:
            if self.workbook is not None:
                self.workbook.reRun()
            protoData = WorkbookUpdateCommonResponse(
                isError = False,
                workbookKey = self.workbook.workbookKey,
                newWorkbook = self.workbook
            )
            eventData = CellEventData(
                workbook = self.workbook,
                cell = self._ic,
                event = P6Events.Cell.Update.event,
                data = protoData
            )
            self.__onCellEvent(eventData)

    @WrapperCell.formula.setter
    def formula(self, newFormula: str):
        self._ic.formula = newFormula
        if self.__onCellEvent is not None:
            if self.workbook is not None:
                self.workbook.reRun()
            protoData = WorkbookUpdateCommonResponse(
                isError = False,
                workbookKey = self.workbook.workbookKey,
                newWorkbook = self.workbook
            )
            eventData = CellEventData(
                workbook = self.workbook,
                cell = self._ic,
                event = P6Events.Cell.Update.event,
                data = protoData
            )
            self.__onCellEvent(eventData)

    def runScript(self, globalScope = None, localScope = None):
        if self.script is not None:
            super().runScript(globalScope, localScope)
            if self.__onCellEvent is not None:
                if self.workbook is not None:
                    self.workbook.reRun()
                protoData = WorkbookUpdateCommonResponse(
                    isError = False,
                    workbookKey = self.workbook.workbookKey,
                    newWorkbook = self.workbook
                )
                eventData = CellEventData(
                    workbook = self.workbook,
                    cell = self._ic,
                    event = P6Events.Cell.Update.event,
                    data = protoData
                )
                self.__onCellEvent(eventData)

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        self._innerCell.script = newScript
        self.runScript(globalScope, localScope)

    def clearScriptResult(self):
        if self.hasScript():
            super().clearScriptResult()
            if self.__onCellEvent is not None:
                if self.workbook is not None:
                    self.workbook.reRun()
                protoData = WorkbookUpdateCommonResponse(
                    isError = False,
                    workbookKey = self.workbook.workbookKey,
                    newWorkbook = self.workbook
                )
                eventData = CellEventData(
                    workbook = self.workbook,
                    cell = self._ic,
                    event = P6Events.Cell.Update.event,
                    data = protoData
                )
                self.__onCellEvent(eventData)

    def reRun(self, globalScope = None, localScope = None):
        self._innerCell.clearScriptResult()
        self._innerCell.runScript(globalScope, localScope)
        if self.__onCellEvent is not None:
            if self.workbook is not None:
                self.workbook.reRun()
            protoData = WorkbookUpdateCommonResponse(
                isError = False,
                workbookKey = self.workbook.workbookKey,
                newWorkbook = self.workbook
            )
            eventData = CellEventData(
                workbook = self.workbook,
                cell = self._ic,
                event = P6Events.Cell.Update.event,
                data = protoData
            )
            self.__onCellEvent(eventData)
