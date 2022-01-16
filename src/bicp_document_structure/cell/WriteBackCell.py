from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.cache.DataCache import DataCache
from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer


class WriteBackCell(Cell):
    """
    A cell decorator that can write back to the container that contains the cell
    """

    def __init__(self, cell:Cell,container:MutableCellContainer):
        self.__innerCell:Cell = cell
        self.__container = container
        self.__pos = cell.address
        self.__colIndex = cell.address.colIndex
        self.__rowIndex = cell.address.rowIndex

    ### >> CacheCell << ###

    @property
    def cache(self) -> DataCache:
        return self.__innerCell.cache

    ### >> Cell << ###
    def bareValue(self):
        return self.__innerCell.bareValue()

    def toJson(self) -> CellJson:
        return self.__innerCell.toJson()

    def setScriptAndRun(self, newScript, globalScope=None, localScope=None):
        self.__innerCell.setScriptAndRun(newScript, globalScope, localScope)
        self.__writeCell()

    def hasCode(self) -> bool:
        return self.__innerCell.hasCode()

    @property
    def displayValue(self) -> str:
        return self.__innerCell.displayValue

    @property
    def value(self):
        return self.__innerCell.value

    @value.setter
    def value(self, newValue):
        self.__innerCell.value = newValue
        self.__writeCell()

    @property
    def script(self) -> str:
        return self.__innerCell.script

    @script.setter
    def script(self, newCode: str):
        self.__innerCell.script = newCode
        self.__writeCell()

    @property
    def address(self) -> CellAddress:
        return self.__innerCell.address

    def __writeCell(self):
        cellNotWritten = not self.__container.hasCellAt(self.__pos)
        if cellNotWritten:
            self.__container.addCell(self.__innerCell)

    @property
    def row(self) -> int:
        return self.__innerCell.row

    @property
    def col(self) -> int:
        return self.__innerCell.col

    def isValueEqual(self, anotherCell):
        return self.__innerCell.isValueEqual(anotherCell)

    def runScript(self, globalScope=None, localScope=None):
        self.__innerCell.runScript(globalScope, localScope)
        self.__writeCell()

    def __eq__(self, o: object) -> bool:
        return self.__innerCell.__eq__(o)
