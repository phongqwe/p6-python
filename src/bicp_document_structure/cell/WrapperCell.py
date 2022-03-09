from abc import ABC

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress


class WrapperCell(Cell, ABC):
    """
    An abstract Cell decorator that wraps around another cell and carries out its work using the inner cell
    """

    def __init__(self, innerCell: Cell):
        self._innerCell: Cell = innerCell

    @property
    def intValue(self) -> int:
        return self._innerCell.intValue

    @property
    def floatValue(self) -> float:
        return self._innerCell.floatValue

    @property
    def strValue(self) -> str:
        return self._innerCell.strValue

    def isValueEqual(self, anotherCellOrValue):
        return self._innerCell.isValueEqual(anotherCellOrValue)

    def isEmpty(self):
        return self._innerCell.isEmpty()

    def reRun(self, globalScope = None, localScope = None):
        self._innerCell.reRun(globalScope, localScope)

    def toJsonDict(self) -> dict:
        return self._innerCell.toJsonDict()

    @property
    def formula(self) -> str:
        return self._innerCell.formula

    @formula.setter
    def formula(self, newFormula: str):
        self._innerCell.formula = newFormula

    def bareValue(self):
        return self._innerCell.bareValue()

    def toJson(self) -> CellJson:
        return self._innerCell.toJson()

    @property
    def displayValue(self) -> str:
        return self._innerCell.displayValue

    @property
    def value(self):
        return self._innerCell.value

    @value.setter
    def value(self, newValue):
        self._innerCell.value = newValue

    @property
    def script(self) -> str:
        return self._innerCell.script

    @script.setter
    def script(self, newCode: str):
        self._innerCell.script = newCode

    @property
    def address(self) -> CellAddress:
        return self._innerCell.address

    def __eq__(self, other):
        return self._innerCell.__eq__(other)

    @property
    def row(self) -> int:
        return self._innerCell.row

    @property
    def col(self) -> int:
        return self._innerCell.col

    def runScript(self, globalScope = None, localScope = None):
        self._innerCell.runScript(globalScope, localScope)

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        self._innerCell.setScriptAndRun(newScript, globalScope, localScope)

    def hasCode(self) -> bool:
        return self._innerCell.hasCode()

    def __hash__(self) -> int:
        return self._innerCell.__hash__()

    def clearScriptResult(self):
        return self._innerCell.clearScriptResult()

    def copyFrom(self, anotherCell: "Cell"):
        self._innerCell.copyFrom(anotherCell)
