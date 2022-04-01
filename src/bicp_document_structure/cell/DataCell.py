from typing import Any, Callable

from bicp_document_structure.app.GlobalScope import getGlobals
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.util.CellUtil import convertExceptionToStr
from bicp_document_structure.code_executor.CodeExecutor import CodeExecutor
from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.communication.proto.DocProto_pb2 import CellProto
from bicp_document_structure.util.Util import default
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result


class DataCell(Cell):
    """
    A Cell that holds some data.
    """

    def __init__(self,
                 address: CellAddress,
                 translatorGetter: Callable[[], FormulaTranslator] | None = None,
                 value: Any = None,
                 formula: str = None,
                 script: str = None):
        self.__value: Any = value
        self.__script: str = script
        self.__addr: CellAddress = address
        self.__scriptAlreadyRun: bool = False
        self.__formula: str = formula
        self.__translatorGetter: Callable[[], FormulaTranslator] | None = translatorGetter

    ### >> Cell << ###

    @property
    def formula(self) -> str:
        return self.__formula

    @formula.setter
    def formula(self, newFormula):
        self.__formula = newFormula
        if self.__translatorGetter is not None:
            newScript = self._translateFormula(newFormula, self.__translatorGetter())
            self.__setScriptWithoutChangingFormula(newScript)

    @staticmethod
    def _translateFormula(formula: str, translator: FormulaTranslator) -> str:
        transResult: Result[str, ErrorReport] = translator.translate(formula)
        if transResult.isOk():
            return transResult.value
        else:
            raise ValueError(str(transResult.err))

    def toProtoObj(self) ->CellProto:
        cellProto = CellProto()
        cellProto.address.CopyFrom(self.address.toProtoObj())
        if self.__value is not None:
            cellProto.value = str(self.__value)
        else:
            cellProto.value = ""

        cellProto.script = default(self.__script,"")
        cellProto.formula = default(self.__formula,"")
        return cellProto

    def bareValue(self):
        return self.__value

    def toJson(self) -> CellJson:
        return CellJson(
            value = self.__value,
            script = self.__script,
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
        shouldRun = self.hasScript() and not self.__scriptAlreadyRun
        if shouldRun:
            # x: this will update self.__value
            self.runScript()
        return self.__value

    @value.setter
    def value(self, newValue):
        self.__value = newValue
        self.__script = None
        self.__formula = None
        self.__scriptAlreadyRun = False

    @property
    def script(self) -> str:
        if self.formula is not None and len(self.formula) != 0:
            if self.__translatorGetter is not None:
                newScript = self._translateFormula(self.formula, self.__translatorGetter())
                self.__script = newScript
        return self.__script

    @script.setter
    def script(self, newScript: str):
        self.__setScriptWithoutChangingFormula(newScript)
        self.__formula = f"=SCRIPT({newScript})"

    def __setScriptWithoutChangingFormula(self, newScript):
        self.__script = newScript
        self.__value = None
        self.__scriptAlreadyRun = False

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
        if self.__script is not None:
            if localScope is None:
                localScope = {}

            if globalScope is None:
                globalScope = getGlobals()
            try:
                codeResult = CodeExecutor.evalCode(self.__script, globalScope, localScope)
            except Exception as e:
                codeResult = e
            self.__value = codeResult
            self.__scriptAlreadyRun = True

    def setScriptAndRun(self, newScript, globalScope = None, localScope = None):
        self.script = newScript
        self.runScript(globalScope, localScope)

    def hasScript(self) -> bool:
        return self.__script is not None and len(self.__script) != 0

    def __hash__(self) -> int:
        return hash((self.__value, self.__script, self.__addr))

    def clearScriptResult(self):
        if self.hasScript():
            self.__value = None
            self.__scriptAlreadyRun = False

    def copyFrom(self, anotherCell: "Cell"):
        self.__value = anotherCell.value
        self.__formula = anotherCell.formula
        self.__script = anotherCell.script
