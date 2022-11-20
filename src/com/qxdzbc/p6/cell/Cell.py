from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional, Any

from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.util.CellUtils import CellUtils
from com.qxdzbc.p6.cell.rpc_data_structure.CellId import CellId
from com.qxdzbc.p6.util.CanCheckEmpty import CanCheckEmpty
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.util.result.Results import Results
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto

if TYPE_CHECKING:
    pass


class Cell(CanCheckEmpty, ToProto[CellProto], ABC):
    """
    Cell interface
    """

    @property
    def id(self) -> CellId:
        return CellId(self.address, self.wbKey, self.wsName)

    @property
    def cellValue(self) -> CellValue:
        raise NotImplementedError()

    @cellValue.setter
    def cellValue(self, newCellValue: CellValue):
        c = CellContent(
            value = newCellValue
        )
        self.content = c

    def __eq__(self, other):
        if isinstance(other, Cell):
            sameValue = self.value == other.value
            sameAddress = self.address == other.address
            return sameValue and sameAddress
        else:
            return False

    @property
    def displayValue(self) -> str:
        raise NotImplementedError()

    @property
    def wsName(self) -> Optional[str]:
        raise NotImplementedError()

    @property
    def wbKey(self) -> Optional[WorkbookKey]:
        raise NotImplementedError()

    @property
    def formula(self) -> str:
        """ the original formula """
        raise NotImplementedError()

    @formula.setter
    def formula(self, newFormula):
        """ set new formula, script will also be updated """
        raise NotImplementedError()

    def setFormula(self,newFormula):
        c = CellContent(
            formula = newFormula
        )
        self.content = c

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
            if isinstance(v, str):
                if CellUtils.isNumericString(v):
                    return v[1:]
                else:
                    return v
            else:
                return str(v)

    @property
    def value(self):
        """ return the value of this cell. This value may be the literal value the cell or holding or the result of the formula of this cell """
        raise NotImplementedError()

    @value.setter
    def value(self, newValue: Any):
        """ set the value of this cell """
        raise NotImplementedError()

    def setValue(self,newValue: Any):
        c = CellContent(
            value = CellValue.fromAny(newValue)
        )
        self.content = c

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

    def copyFromRs(self, anotherCell: CellId) -> Result[None, ErrorReport]:
        """copy everything (data, format, etc.) from another cell to this cell"""
        raise NotImplementedError()

    def copyFrom(self, anotherCell: CellId):
        """copy everything (data, format, etc.) from another cell to this cell"""
        Results.extractOrRaise(self.copyFromRs(anotherCell))

    def copyFromCellRs(self, anotherCell: Cell) -> Result[None, ErrorReport]:
        """copy everything (data, format, etc.) from another cell to this cell"""
        raise NotImplementedError()

    def copyFromCell(self, anotherCell: Cell):
        """copy everything (data, format, etc.) from another cell to this cell"""
        Results.extractOrRaise(self.copyFromCellRs(anotherCell))

    @property
    def rootCell(self) -> 'Cell':
        raise NotImplementedError()

    @property
    def content(self) -> CellContent:
        """extract a CellContent object from this cell"""
        raise NotImplementedError()

    @content.setter
    def content(self, newContent: CellContent):
        raise NotImplementedError()

    def toProtoObj(self) -> CellProto:
        # v = None
        # if self.cellValue:
        #     if self.cellValue.isNotEmpty():
        #         v = self.cellValue.toProtoObj()
        # f = self.formula
        c = self.content.toProtoObj()
        return CellProto(
            id = self.id.toProtoObj(),
            # value = v,
            # formula = f,
            content = c
        )
