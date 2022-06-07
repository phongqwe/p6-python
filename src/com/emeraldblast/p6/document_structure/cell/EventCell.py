from typing import Callable

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.WrapperCell import WrapperCell
from com.emeraldblast.p6.document_structure.communication.event.P6Events import P6Events
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.EventData import EventData


class EventCell(WrapperCell):

    """
    A cell wrapper that trigger event reactors at certain events
    """

    def __init__(self,
                 innerCell: Cell,
                 onCellEvent: Callable[[EventData], None] = None):
        super().__init__(innerCell)
        self.__onCellEvent = onCellEvent
        self._ic = innerCell

    @WrapperCell.value.setter
    def value(self, newValue):
        self._innerCell.value = newValue
        if self.__onCellEvent is not None:
            if self.workbook is not None:
                self.workbook.reRun()
            protoData = P6Events.Cell.Update.Response(
                isError=False,
                workbookKey = self.workbook.workbookKey,
                newWorkbook = self.workbook)
            self.__onCellEvent(protoData.toEventData())

    @WrapperCell.script.setter
    def script(self, newScript: str):
        self._innerCell.script = newScript
        if self.__onCellEvent is not None:
            if self.workbook is not None:
                self.workbook.reRun()
            protoData = P6Events.Cell.Update.Response(
                isError = False,
                workbookKey = self.workbook.workbookKey,
                newWorkbook = self.workbook
            )
            self.__onCellEvent(protoData.toEventData())

    @WrapperCell.formula.setter
    def formula(self, newFormula: str):
        self._ic.formula = newFormula
        if self.__onCellEvent is not None:
            if self.workbook is not None:
                self.workbook.reRun()
            protoData = P6Events.Cell.Update.Response(
                isError = False,
                workbookKey = self.workbook.workbookKey,
                newWorkbook = self.workbook
            )
            self.__onCellEvent(protoData.toEventData())

    def runScript(self, globalScope = None, localScope = None):
        if self.script is not None:
            super().runScript(globalScope, localScope)
            if self.__onCellEvent is not None:
                if self.workbook is not None:
                    self.workbook.reRun()
                protoData = P6Events.Cell.Update.Response(
                    isError = False,
                    workbookKey = self.workbook.workbookKey,
                    newWorkbook = self.workbook
                )
                self.__onCellEvent(protoData.toEventData())

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        self._innerCell.script = newScript
        self.runScript(globalScope, localScope)

    def clearScriptResult(self):
        if self.hasScript():
            super().clearScriptResult()
            if self.__onCellEvent is not None:
                if self.workbook is not None:
                    self.workbook.reRun()
                protoData = P6Events.Cell.Update.Response(
                    isError = False,
                    workbookKey = self.workbook.workbookKey,
                    newWorkbook = self.workbook
                )
                self.__onCellEvent(protoData.toEventData())

    def reRun(self, globalScope = None, localScope = None,refreshScript:bool=False):
        self.rootCell.reRun(globalScope, localScope,refreshScript)
        if self.__onCellEvent is not None:
            if self.workbook is not None:
                self.workbook.reRun()
            protoData = P6Events.Cell.Update.Response(
                isError = False,
                workbookKey = self.workbook.workbookKey,
                newWorkbook = self.workbook
            )
            self.__onCellEvent(protoData.toEventData())
