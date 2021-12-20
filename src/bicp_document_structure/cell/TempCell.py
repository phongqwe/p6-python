from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.DataCell import DataCell
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer


class TempCell(Cell):
    """
    act as a temporary cell returned by querying non-existing cell from a CellHolder.
    Only write object to the holder when the content of the temp cell is mutated.
    """

    def __init__(self, holder: MutableCellContainer, address: CellAddress):
        self.__pos = address
        self.__colIndex = address.colIndex
        self.__rowIndex = address.rowIndex
        self.__holder = holder
        self.__innerCell = None
        if holder.hasCellAt(address):
            self.__innerCell = holder.getCell(address)
        else:
            self.__innerCell = DataCell(address)

    ### >> Cell << ###
    def setCodeAndRun(self, newCode, globalScope, localScope=None):
        self.__innerCell.setCodeAndRun(newCode, globalScope, localScope)

    def hasCode(self) -> bool:
        return self.__innerCell.hasCode()

    @property
    def value(self):
        return self.__innerCell.value

    @value.setter
    def value(self, newValue):
        self.__innerCell.value = newValue
        self.__writeCell()

    @property
    def code(self) -> str:
        return self.__innerCell.code

    @code.setter
    def code(self, newCode: str):
        self.__innerCell.code = newCode
        self.__writeCell()

    @property
    def address(self) -> CellAddress:
        return self.__innerCell.address

    def __writeCell(self):
        cellNotWritten = not self.__holder.hasCellAt(self.__pos)
        if cellNotWritten:
            self.__holder.addCell(self.__innerCell)

    @property
    def row(self) -> int:
        return self.__innerCell.row

    @property
    def col(self) -> int:
        return self.__innerCell.col

    def isValueEqual(self, anotherCell):
        return self.__innerCell.isValueEqual(anotherCell)

    def runCode(self, globalScope=None, localScope=None):
        self.__innerCell.runCode(globalScope, localScope)
        self.__writeCell()

    def __eq__(self, o: object) -> bool:
        return self.__innerCell.__eq__(o)
