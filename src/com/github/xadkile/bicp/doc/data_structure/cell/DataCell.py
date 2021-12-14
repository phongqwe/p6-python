from com.github.xadkile.bicp.doc.data_structure.cell.Cell import Cell
from com.github.xadkile.bicp.doc.data_structure.cell.position.CellPosition import CellPosition


class DataCell(Cell):
    """
    a cell that holds some data
    """

    def __init__(self, position: CellPosition, value=None, code: str = ""):
        self.__value = value
        self.__code: str = code
        self.__pos = position

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

    def isValueEqual(self, anotherCell):
        return self.value == anotherCell.value

    def pos(self) -> CellPosition:
        return self.__pos
