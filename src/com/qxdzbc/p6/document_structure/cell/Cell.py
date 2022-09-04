from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional

from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto

from com.qxdzbc.p6.document_structure.cell.CellContent import CellContent
from com.qxdzbc.p6.document_structure.cell.CellJson import CellJson
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.cell.util.CellUtils import CellUtils
from com.qxdzbc.p6.document_structure.util.ToJson import ToJson
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto

if TYPE_CHECKING:
    from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet
    from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook

class Cell(ToJson, ToProto[CellProto], ABC):
    """
    Cell interface
    """

    def __eq__(self, other):
        if isinstance(other, Cell):
            sameValue = self.value == other.value
            sameScript = self.script == other.script or (not (self.script and other.script))
            sameAddress = self.address == other.address
            return sameValue and sameScript and sameAddress
        else:
            return False

    @property
    def sourceValue(self)->str:
        """:return the source of the value of this cell. That is either formula (if this is a formulaic cell) or value if this is a value cell"""
        raise NotImplementedError()

    @property
    def displayValue(self)->str:
        raise NotImplementedError()

    @property
    def worksheet(self) -> Optional[Worksheet]:
        raise NotImplementedError()

    @worksheet.setter
    def worksheet(self, newWorksheet: Optional[Worksheet]):
        raise NotImplementedError()

    def removeFromWorksheet(self):
        self.worksheet = None

    @property
    def workbook(self)->Optional[Workbook]:
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
        v = self.value
        if v is None:
            return ""
        else:
            if isinstance(v,str):
                if CellUtils.isNumericString(v):
                    return v[1:]
                else:
                    return v
            else:
                return str(v)

    @property
    def bareScript(self)->str:
        """
        :return: the bare script, may not be consistent with the result of running the formula of this cell.
        """
        raise NotImplementedError()

    @property
    def bareFormula(self)->str:
        """
        :return: the bare formula, may not be consistent with the result of running the script of this cell.
        """
        raise NotImplementedError()

    @property
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
        """ return the script hold by this cell. Script is always Python. The script is guranteed to be always updated"""
        raise NotImplementedError()

    @script.setter
    def script(self, newScript: str):
        """ set the script hold by this cell. Script is always Python.
            @deprecated: don't use
        """
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

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        """set new script for this cell and execute it immediately"""
        raise NotImplementedError()

    def hasScript(self) -> bool:
        """:return True if this cell contains any script"""
        raise NotImplementedError()

    def toJson(self) -> CellJson:
        raise NotImplementedError()

    def clearScriptResult(self):
        """delete script result if this Cell houses any script"""
        raise NotImplementedError()

    def isEmpty(self):
        if self.hasScript():
            return True
        else:
            return self.value is not None

    def reRun(self, globalScope = None, localScope = None, refreshScript:bool =False):
        if refreshScript:
            self.refreshScript()
        self.clearScriptResult()
        self.runScript(globalScope, localScope)

    def refreshScript(self):
        z = self.script

    def copyFrom(self, anotherCell: "Cell"):
        """copy everything (data, format, etc.) from another cell to this cell"""
        raise NotImplementedError()

    def toJsonDict(self) -> dict:
        return self.toJson().toJsonDict()

    @property
    def rootCell(self)->'Cell':
        raise NotImplementedError()

    @property
    def content(self)->CellContent:
        """extract a CellContent object from this cell"""
        raise NotImplementedError()

    @content.setter
    def content(self,newContent:CellContent):
        raise NotImplementedError()
