from abc import ABC
from typing import Optional

from com.qxdzbc.p6.cell.Cell import Cell
from com.qxdzbc.p6.cell.CellContent import CellContent
from com.qxdzbc.p6.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.cell.rpc_data_structure.CellId import CellId
from com.qxdzbc.p6.cell.rpc_data_structure.CellValue import CellValue
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto


class WrapperCell(Cell):
    """
    An abstract Cell decorator that wraps around another cell and carries out its work using the inner cell
    """

    @property
    def cellValue(self) -> CellValue:
        return self.rootCell.cellValue

    @property
    def wsName(self) -> Optional[str]:
        return self.rootCell.wsName

    @property
    def wbKey(self) -> Optional[WorkbookKey]:
        return self.rootCell.wbKey

    def copyFromRs(self, anotherCell: CellId) -> Result[None, ErrorReport]:
        return self.rootCell.copyFromRs(anotherCell)

    def copyFromCellRs(self, anotherCell: Cell) -> Result[None, ErrorReport]:
        pass

    @property
    def innerCell(self)->'Cell':
        return self._innerCell

    def __init__(self, innerCell: Cell):
        self._innerCell: Cell = innerCell

    @property
    def rootCell(self) -> 'Cell':
        return self._innerCell.rootCell

    @property
    def content(self) -> CellContent:
        return self.rootCell.content

    @content.setter
    def content(self, newContent: CellContent):
        self.rootCell.content = newContent

    def toProtoObj(self) -> CellProto:
        return self.rootCell.toProtoObj()

    @property
    def intValue(self) -> int:
        return self.rootCell.intValue

    @property
    def floatValue(self) -> float:
        return self.rootCell.floatValue

    @property
    def strValue(self) -> str:
        return self.rootCell.strValue

    def isValueEqual(self, anotherCellOrValue):
        return self.rootCell.isValueEqual(anotherCellOrValue)

    def isEmpty(self):
        return self.rootCell.isEmpty()

    @property
    def formula(self) -> str:
        return self.rootCell.formula

    @formula.setter
    def formula(self, newFormula: str):
        self.rootCell.formula = newFormula

    @property
    def displayText(self) -> str:
        return self.rootCell.displayText

    @property
    def value(self):
        return self.rootCell.value

    @value.setter
    def value(self, newValue):
        self.rootCell.value = newValue

    @property
    def address(self) -> CellAddress:
        return self.rootCell.address

    def __eq__(self, other):
        return self.rootCell.__eq__(other)

    @property
    def row(self) -> int:
        return self.rootCell.row

    @property
    def col(self) -> int:
        return self.rootCell.col

    def __hash__(self) -> int:
        return self.rootCell.__hash__()

    def copyFrom(self, anotherCell: CellId):
        self.rootCell.copyFrom(anotherCell)
