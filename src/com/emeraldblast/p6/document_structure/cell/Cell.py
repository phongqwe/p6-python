from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from com.emeraldblast.p6.document_structure.cell.CellJson import CellJson
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.util.ToJson import ToJson
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.proto.DocProtos_pb2 import CellProto

if TYPE_CHECKING:
    from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
    from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook

class Cell(ToJson, ToProto[CellProto], ABC):
    """
    Cell interface
    """

    @property
    def worksheet(self) -> Worksheet | None:
        raise NotImplementedError()

    @worksheet.setter
    def worksheet(self, newWorksheet: Worksheet | None):
        raise NotImplementedError()

    def removeFromWorksheet(self):
        self.worksheet = None

    @property
    def workbook(self)->Workbook | None:
        if self.worksheet is not None:
            return self.worksheet.workbook
        else:
            return None

    @property
    def formula(self) -> str:
        """ the original formula """
        raise NotImplementedError()

    @formula.setter
    def formula(self, newFormula):
        """ set new formula, script will also be updated """
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
        # return str(self.value)
        if self.value is None:
            return ""
        else:
            return str(self.value)

    @property
    def displayValue(self) -> str:
        """string representation of the object stored in this cell"""
        raise NotImplementedError()

    def bareScript(self)->str:
        """
        :return: the bare script, may not be consistent with the result of running the formula of this cell.
        """
        raise NotImplementedError()

    def bareFormula(self)->str:
        """
        :return: the bare formula, may not be consistent with the result of running the script of this cell.
        """
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
    def script(self, newScript: str):
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

    def runScript(self, globalScope = None, localScope = None):
        """run the script """
        raise NotImplementedError()

    # def runScriptEventFree(self, globalScope=None, localScope=None):
    #     """run the script without triggering event reactors """
    #     raise NotImplementedError()

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        """set new script for this cell and execute it immediately"""
        raise NotImplementedError()

    # def setScriptAndRunEventFree(self, newScript, globalScope=None, localScope=None):
    #     """set new script for this cell and execute it immediately"""
    #     raise NotImplementedError()

    def hasScript(self) -> bool:
        """:return True if this cell contains any script"""
        raise NotImplementedError()

    def toJson(self) -> CellJson:
        raise NotImplementedError()

    def clearScriptResult(self):
        """delete script result if this Cell houses any script"""
        raise NotImplementedError()

    # def clearScriptResultEventFree(self):
    #     """delete script result if this Cell houses any script without triggering event reactors"""
    #     raise NotImplementedError()

    def isEmpty(self):
        if self.hasScript():
            return True
        else:
            return self.value is not None

    def reRun(self, globalScope = None, localScope = None):
        self.clearScriptResult()
        self.runScript(globalScope, localScope)

    # def reRunEventFree(self, globalScope=None, localScope=None):
    #     self.clearScriptResultEventFree()
    #     self.runScriptEventFree(globalScope, localScope)

    def copyFrom(self, anotherCell: "Cell"):
        """copy everything (data, format, etc.) from another cell to this cell"""
        raise NotImplementedError()

    def toJsonDict(self) -> dict:
        return self.toJson().toJsonDict()