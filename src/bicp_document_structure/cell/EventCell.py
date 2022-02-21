from typing import Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.WrapperCell import WrapperCell
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.P6Events import P6Events


class EventCell(WrapperCell):
    """
    A cell wrapper that trigger event reactors at certain events
    """

    def __init__(self,
                 innerCell: Cell,
                 onCellChange: Callable[[Cell, P6Event], None] = None):
        super().__init__(innerCell)
        self.__onCellChange = onCellChange

    @WrapperCell.value.setter
    def value(self, newValue):
        self._innerCell.value = newValue
        if self.__onCellChange is not None:
            self.__onCellChange(self, P6Events.Cell.UpdateValue)

    @WrapperCell.script.setter
    def script(self, newCode: str):
        self._innerCell.script = newCode
        if self.__onCellChange is not None:
            self.__onCellChange(self, P6Events.Cell.UpdateScript)

    def runScript(self, globalScope = None, localScope = None):
        if self.script is not None:
            super().runScript(globalScope, localScope)
            if self.__onCellChange is not None:
                self.__onCellChange(self, P6Events.Cell.UpdateValue)

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        self._innerCell.script = newScript
        self.runScript(globalScope, localScope)

    def clearScriptResult(self):
        if self.hasCode():
            super().clearScriptResult()
            if self.__onCellChange is not None:
                self.__onCellChange(self, P6Events.Cell.ClearScriptResult)

    def reRun(self, globalScope = None, localScope = None):
        self.clearScriptResult()
        self.runScript(globalScope, localScope)
