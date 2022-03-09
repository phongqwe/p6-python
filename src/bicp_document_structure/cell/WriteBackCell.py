from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.WrapperCell import WrapperCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer


class WriteBackCell(
    WrapperCell
):
    """
    A cell decorator that can write back to the container that contains the cell
    """

    def __init__(self, cell: Cell, container: MutableCellContainer):
        super().__init__(cell)
        self.__innerCell: Cell = cell
        self.__container: MutableCellContainer = container
        self.__pos: CellAddress = cell.address
        self.__colIndex: int = cell.address.colIndex
        self.__rowIndex: int = cell.address.rowIndex

    ### >> Cell << ###

    @WrapperCell.formula.setter
    def formula(self, newFormula: str):
        self.__innerCell.formula=newFormula
        self.__writeCell()

    def clearScriptResult(self):
        self.__innerCell.clearScriptResult()
        if not self.isEmpty():
            self.__writeCell()

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        self.__innerCell.setScriptAndRun(newScript, globalScope, localScope)
        self.__writeCell()

    @property
    def value(self):
        v = self.__innerCell.value
        self.__writeCell()
        return v

    @value.setter
    def value(self, newValue):
        self.__innerCell.value = newValue
        self.__writeCell()

    @WrapperCell.script.setter
    def script(self, newCode: str):
        # x: only add new code if the new code is not empty
        self.__innerCell.script = newCode
        self.__writeCell()

    def __writeCell(self):
        cellNotWritten = not self.__container.hasCellAt(self.__pos)
        if cellNotWritten:
            self.__container.addCell(self.__innerCell)

    def runScript(self, globalScope = None, localScope = None):
        self.__innerCell.runScript(globalScope, localScope)
        self.__writeCell()
