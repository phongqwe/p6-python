from abc import ABC

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress


class Cell(ABC):
    """
    Cell interface
    """

    @property
    def intValue(self) -> int:
        """get cell value as int"""
        return int(self.value)

    @property
    def floatValue(self) -> float:
        """get cell value as float"""
        return float(self.value)

    @property
    def strValue(self) -> str:
        """get cell value as string"""
        return str(self.value)

    @property
    def displayValue(self) -> str:
        """string representation of the object stored in this cell"""
        raise NotImplementedError()

    def bareValue(self):
        """
        :return: the bare value, may not be consistent with the result of running the code of this cell.
        """
        raise NotImplementedError()

    @property
    def value(self):
        """ return the value of this cell """
        raise NotImplementedError()

    @value.setter
    def value(self, newValue):
        """ set the value of this cell """
        raise NotImplementedError()

    @property
    def script(self) -> str:
        """ return the script hold by this cell. Script is always Python"""
        raise NotImplementedError()

    @script.setter
    def script(self, newCode: str):
        """ set the script hold by this cell. Script is always Python"""
        raise NotImplementedError()

    @property
    def address(self) -> CellAddress:
        raise NotImplementedError()

    @property
    def row(self) -> int:
        return self.address.rowIndex

    @property
    def col(self) -> int:
        return self.address.colIndex

    def isValueEqual(self, anotherCell):
        return self.value == anotherCell.value

    def runScript(self, globalScope=None, localScope=None):
        """run the script """
        raise NotImplementedError()

    def setScriptAndRun(self, newScript, globalScope=None, localScope=None):
        """set new code for this cell and execute it immediately"""
        raise NotImplementedError()

    def hasCode(self) -> bool:
        """:return True if this cell contain any code"""
        raise NotImplementedError()

    def toJson(self) -> CellJson:
        raise NotImplementedError()

    def clearScriptResult(self):
        """remove script result if this Cell houses any script"""
        raise NotImplementedError()
