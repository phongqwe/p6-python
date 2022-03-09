from typing import Any

from bicp_document_structure.app.GlobalScope import getGlobals
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.util.CellUtil import convertExceptionToStr
from bicp_document_structure.code_executor.CodeExecutor import CodeExecutor
from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result


class DataCell(Cell):
    """
    A Cell that holds some data.
    """

    def __init__(self,
                 address: CellAddress,
                 value: Any = None,
                 formula: str = None,
                 script: str = None):
        self.__value: Any = value
        self.__code: str = script
        self.__addr: CellAddress = address
        self.__scriptAlreadyRun: bool = False
        self.__formula: str = formula

    ### >> Cell << ###

    @property
    def formula(self) -> str:
        return self.__formula

    def setFormula(self, newFormula: str, formulaTranslator: FormulaTranslator):
        self.__formula = newFormula
        self.script = self.__translateFormula(newFormula, formulaTranslator)

    @staticmethod
    def __translateFormula(formula: str, translator: FormulaTranslator) -> str:
        transResult: Result[str, ErrorReport] = translator.translate(formula)
        if transResult.isOk():
            return transResult.value
        else:
            raise ValueError(str(transResult.err))

    def bareValue(self):
        return self.__value

    def toJson(self) -> CellJson:
        return CellJson(
            value = self.__value,
            script = self.__code,
            formula = self.__formula,
            address = self.__addr.toJson(),
        )

    @property
    def displayValue(self) -> str:
        if isinstance(self.value, Exception):
            return convertExceptionToStr(self.__value)
        else:
            str(self.__value)

    @property
    def value(self):
        """
        get the value contained in this cell.
        If this cell contains script, the script will run and the updated value will be returned
        """
        shouldRun = self.hasCode() and not self.__scriptAlreadyRun
        if shouldRun:
            # x: this will update self.__value
            self.runScript()
        return self.__value

    @value.setter
    def value(self, newValue):
        self.__value = newValue
        self.__code = None
        self.__scriptAlreadyRun = False

    @property
    def script(self) -> str:
        return self.__code

    @script.setter
    def script(self, newCode: str):
        self.__code = newCode
        self.__value = None
        self.__scriptAlreadyRun = False
        self.__formula = f"=SCRIPT({newCode})"

    @property
    def address(self) -> CellAddress:
        return self.__addr

    def __eq__(self, other):
        if isinstance(other, Cell):
            sameValue = self.value == other.value
            sameCode = self.script == other.script
            sameAddress = self.address == other.address
            return sameValue and sameCode and sameAddress
        else:
            return False

    @property
    def row(self) -> int:
        return self.__addr.rowIndex

    @property
    def col(self) -> int:
        return self.__addr.colIndex

    def runScript(self, globalScope = None, localScope = None):
        if self.script is not None:
            if localScope is None:
                localScope = {}

            if globalScope is None:
                globalScope = getGlobals()
            try:
                codeResult = CodeExecutor.evalCode(self.script, globalScope, localScope)
            except Exception as e:
                codeResult = e
            self.__value = codeResult
            self.__scriptAlreadyRun = True

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        self.script = newScript
        self.runScript(globalScope, localScope)

    def hasCode(self) -> bool:
        return self.__code is not None and len(self.__code) != 0

    def __hash__(self) -> int:
        return hash((self.__value, self.__code, self.__addr))

    def clearScriptResult(self):
        if self.hasCode():
            self.__value = None
            self.__scriptAlreadyRun = False

    def copyFrom(self, anotherCell: "Cell"):
        self.__value = anotherCell.value
        self.__formula = anotherCell.formula
        self.__code = anotherCell.script
