from typing import Callable

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.WrapperCell import WrapperCell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer


class WriteBackCell(WrapperCell):
    """
    A cell decorator that can write itself into to its container when its content (value,formula,script) is changed.
    """

    def __init__(self, cell: Cell, container: MutableCellContainer, onChange: Callable[[Cell], None] | None = None):
        """

        :param cell:
        :param container:
        :param onChange: a function that will be triggered whenever this cell's content is changed
        """
        super().__init__(cell)
        self.__container: MutableCellContainer = container
        self.__pos: CellAddress = cell.address
        self.__colIndex: int = cell.address.colIndex
        self.__rowIndex: int = cell.address.rowIndex
        self.__onChange = onChange

    ### >> Cell << ###

    @WrapperCell.formula.setter
    def formula(self, newFormula: str):
        self.innerCell.formula=newFormula
        self.__writeBack()

    def copyFrom(self, anotherCell: "Cell"):
        self.innerCell.copyFrom(anotherCell)
        self.__writeBack()

    def clearScriptResult(self):
        self.innerCell.clearScriptResult()
        if not self.isEmpty():
            self.__writeBack()

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        self.innerCell.setScriptAndRun(newScript, globalScope, localScope)
        self.__writeBack()

    @WrapperCell.value.setter
    def value(self, newValue):
        self.innerCell.value = newValue
        self.__writeBack()

    @WrapperCell.script.setter
    def script(self, newScript: str):
        # x: only add new code if the new code is not empty
        self.innerCell.script = newScript
        self.__writeBack()

    def __writeBack(self):
        """write the self into the container"""
        cellNotWritten = not self.__container.hasCellAt(self.__pos)
        if cellNotWritten:
            self.__container.addCell(self.innerCell)
        if self.__onChange:
            self.__onChange(self.rootCell)

    def runScript(self, globalScope = None, localScope = None):
        self.innerCell.runScript(globalScope, localScope)
        self.__writeBack()
