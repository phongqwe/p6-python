from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional

from com.qxdzbc.p6.document_structure.cell.CellContent import CellContent
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.cell.util.CellUtils import CellUtils
from com.qxdzbc.p6.document_structure.util.CanCheckEmpty import CanCheckEmpty
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.util.result.Results import Results
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellValue import CellValue

if TYPE_CHECKING:
    pass


class Cell(CanCheckEmpty,ABC):
    """
    Cell interface
    """

    @property
    def id(self) -> CellId:
        return CellId(self.address, self.wbKey, self.wsName)
    @property
    def cellValue(self)->CellValue:
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, Cell):
            sameValue = self.value == other.value
            sameAddress = self.address == other.address
            return sameValue and sameAddress
        else:
            return False

    @property
    def displayValue(self)->str:
        raise NotImplementedError()

    @property
    def wsName(self) -> Optional[str]:
        raise NotImplementedError()

    @property
    def wbKey(self)->Optional[WorkbookKey]:
        raise NotImplementedError()

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

    def isEmpty(self):
        raise NotImplementedError()

    def copyFromRs(self, anotherCell: CellId)->Result[None,ErrorReport]:
        """copy everything (data, format, etc.) from another cell to this cell"""
        raise NotImplementedError()

    def copyFrom(self, anotherCell: CellId):
        """copy everything (data, format, etc.) from another cell to this cell"""
        Results.extractOrRaise(self.copyFromRs(anotherCell))

    def copyFromCellRs(self, anotherCell: Cell)->Result[None,ErrorReport]:
        """copy everything (data, format, etc.) from another cell to this cell"""
        raise NotImplementedError()

    def copyFromCell(self, anotherCell: Cell):
        """copy everything (data, format, etc.) from another cell to this cell"""
        Results.extractOrRaise(self.copyFromCellRs(anotherCell))

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
