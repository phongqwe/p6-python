from abc import ABC

from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress


class Cell(ABC):
    """
    Cell interface
    """
    @property
    def formula(self)->str:
        """ the original formula """
        raise NotImplementedError()
    @formula.setter
    def formula(self,newFormula):
        """ set new formula """
        raise NotImplementedError()

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
        :return: the bare value, may not be consistent with the result of running the script of this cell.
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

    def isValueEqual(self, anotherCellOrValue):
        if isinstance(anotherCellOrValue, Cell):
            return self.value == anotherCellOrValue.value
        else:
            return self.value == anotherCellOrValue

    def runScript(self, globalScope=None, localScope=None):
        """run the script """
        raise NotImplementedError()

    def setScriptAndRun(self, newScript, globalScope=None, localScope=None):
        """set new script for this cell and execute it immediately"""
        raise NotImplementedError()

    def hasCode(self) -> bool:
        """:return True if this cell contain any script"""
        raise NotImplementedError()

    def toJson(self) -> CellJson:
        raise NotImplementedError()

    def clearScriptResult(self):
        """delete script result if this Cell houses any script"""
        raise NotImplementedError()

    def isEmpty(self):
        if self.hasCode():
            return True
        else:
            return self.value is not None

    def reRun(self, globalScope=None, localScope=None):
        self.clearScriptResult()
        self.runScript(globalScope, localScope)