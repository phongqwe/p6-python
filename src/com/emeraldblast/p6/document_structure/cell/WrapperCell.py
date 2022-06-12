from abc import ABC

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.CellContent import CellContent
from com.emeraldblast.p6.document_structure.cell.CellJson import CellJson
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.proto.DocProtos_pb2 import CellProto


class WrapperCell(Cell, ABC):
    """
    An abstract Cell decorator that wraps around another cell and carries out its work using the inner cell
    """

    @property
    def innerCell(self)->'Cell':
        return self._innerCell

    def __init__(self, innerCell: Cell):
        self._innerCell: Cell = innerCell

    @property
    def sourceValue(self) -> str:
        return self.rootCell.sourceValue

    @property
    def rootCell(self) -> 'Cell':
        return self._innerCell.rootCell

    @property
    def content(self) -> CellContent:
        return self.rootCell.content

    @content.setter
    def content(self, newContent: CellContent):
        self.rootCell.content = newContent

    @property
    def worksheet(self) -> Worksheet | None:
        return self.rootCell.worksheet

    @worksheet.setter
    def worksheet(self, newWorksheet: Worksheet | None):
        self.rootCell.worksheet = newWorksheet

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

    def reRun(self, globalScope = None, localScope = None, refreshScript:bool =False):
        self.rootCell.reRun(globalScope, localScope,refreshScript)

    def toJsonDict(self) -> dict:
        return self.rootCell.toJsonDict()

    @property
    def formula(self) -> str:
        return self.rootCell.formula

    @formula.setter
    def formula(self, newFormula: str):
        self.rootCell.formula = newFormula

    @property
    def bareScript(self) -> str:
        return self.rootCell.bareScript

    @property
    def bareFormula(self) -> str:
        return self.rootCell.bareFormula

    @property
    def bareValue(self):
        return self.rootCell.bareValue

    def toJson(self) -> CellJson:
        return self.rootCell.toJson()

    @property
    def displayValue(self) -> str:
        return self.rootCell.displayValue

    @property
    def value(self):
        return self.rootCell.value

    @value.setter
    def value(self, newValue):
        self.rootCell.value = newValue

    @property
    def script(self) -> str:
        return self.rootCell.script

    @script.setter
    def script(self, newScript: str):
        self.rootCell.script = newScript

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

    def runScript(self, globalScope = None, localScope = None):
        self.rootCell.runScript(globalScope, localScope)

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        self.rootCell.setScriptAndRun(newScript, globalScope, localScope)

    def hasScript(self) -> bool:
        return self.rootCell.hasScript()

    def __hash__(self) -> int:
        return self.rootCell.__hash__()

    def clearScriptResult(self):
        return self.rootCell.clearScriptResult()

    def copyFrom(self, anotherCell: "Cell"):
        self.rootCell.copyFrom(anotherCell)
