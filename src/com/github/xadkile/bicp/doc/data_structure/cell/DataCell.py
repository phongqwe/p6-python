from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.address.CellAddress import CellAddress


class DataCell(Cell):
    """
    a cell that holds some data
    """

    def __init__(self, address: CellAddress, value=None, code: str = ""):
        self.__value = value
        self.__code: str = code
        self.__addr = address

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newValue):
        self.__value = newValue

    @property
    def code(self) -> str:
        return self.__code

    @code.setter
    def code(self, newCode: str):
        self.__code = newCode

    @property
    def address(self) -> CellAddress:
        return self.__addr

    def isValueEqual(self, anotherCell):
        return self.value == anotherCell.value
