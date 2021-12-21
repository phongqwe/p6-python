from abc import ABC

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress


class Cell(ABC):
    """
    Cell interface
    """

    @property
    def numericValue(self)->float:
        return float(self.value)

    @property
    def strValue(self)->str:
        return str(self.value)


    @property
    def displayValue(self)->str:
        """string representation of the object stored in this cell"""
        raise NotImplementedError()

    def _bareValue(self):
        """
        For debugging only
        :return: the bare value, may not be consistent with the result of running the code of this cell.
        """
        raise NotImplementedError()

    @property
    def value(self):
        raise NotImplementedError()

    @value.setter
    def value(self,newValue):
        raise NotImplementedError()

    @property
    def code(self)->str:
        raise NotImplementedError()

    @code.setter
    def code(self,newCode:str):
        raise NotImplementedError()

    @property
    def address(self)->CellAddress:
        raise NotImplementedError()

    @property
    def row(self) -> int:
        return self.address.rowIndex

    @property
    def col(self) -> int:
        return self.address.colIndex

    def isValueEqual(self, anotherCell):
        return self.value == anotherCell.value

    def runCode(self, globalScope=None, localScope=None):
        raise NotImplementedError()

    def setCodeAndRun(self,newCode,globalScope=None, localScope=None):
        """set new code for this cell and execute it immediately"""
        raise NotImplementedError()

    def hasCode(self)->bool:
        """:return True if this cell contain any code"""
        raise NotImplementedError()

    def toJson(self)->CellJson:
        raise NotImplementedError()