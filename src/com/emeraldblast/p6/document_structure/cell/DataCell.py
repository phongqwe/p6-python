from typing import Any, Callable

from com.emeraldblast.p6.document_structure.app.GlobalScope import getGlobals
from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.CellContent import CellContent
from com.emeraldblast.p6.document_structure.cell.CellContentImp import CellContentImp
from com.emeraldblast.p6.document_structure.cell.CellJson import CellJson
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell.util.CellUtil import convertExceptionToStr
from com.emeraldblast.p6.document_structure.code_executor.CodeExecutor import CodeExecutor
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.emeraldblast.p6.document_structure.util.Util import default
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.proto.DocProtos_pb2 import CellProto


class DataCell(Cell):
    """
    A Cell that holds some data.
    """

    @property
    def rootCell(self) -> 'Cell':
        return self

    @property
    def content(self) -> CellContent:
        v = self.value
        if self.formula or self.script:
            v = None
        return CellContentImp(
            value = v,
            formula = self.formula,
            script = self.script
        )

    @content.setter
    def content(self, newContent: CellContent):
        self.__value = newContent.value
        self.__formula = newContent.formula
        self.__script = newContent.script

    texualType = [int, float, str]
    @property
    def bareScript(self) -> str:
        return self.__script

    @property
    def bareFormula(self) -> str:
        return self.__formula

    def __init__(self,
                 address: CellAddress,
                 value: Any = None,
                 formula: str = None,
                 script: str = None,
                 worksheet: Worksheet | None = None):
        self.__value: Any = value
        self.__script: str = script
        self.__formula: str = formula
        self.__scriptAlreadyRun: bool = False
        self.__addr: CellAddress = address

        def translatorGetter():
            if self.workbook is not None and self.worksheet is not None:
                return self.workbook.getTranslator(self.worksheet.name)
            else:
                return None

        self.__translatorGetter: Callable[[], FormulaTranslator] | None = translatorGetter
        self.__ws: Worksheet | None = worksheet

    ### >> Cell << ###

    @property
    def worksheet(self) -> Worksheet | None:
        return self.__ws

    @worksheet.setter
    def worksheet(self, newWorksheet: Worksheet | None):
        self.__ws = newWorksheet

    @property
    def formula(self) -> str:
        return self.__formula

    @formula.setter
    def formula(self, newFormula):
        if newFormula != self.__formula:
            self.__formula = newFormula
            if self.__translatorGetter is not None:
                translator = self.__translatorGetter()
                if translator is not None:
                    newScript = self._translateFormula(newFormula, translator)
                    self.__setScriptWithoutChangingFormula(newScript)

    @staticmethod
    def _translateFormula(formula: str, translator: FormulaTranslator) -> str:
        transResult: Result[str, ErrorReport] = translator.translate(formula)
        if transResult.isOk():
            return transResult.value
        else:
            raise ValueError(str(transResult.err))

    def toProtoObj(self) -> CellProto:
        cellProto = CellProto()
        cellProto.address.CopyFrom(self.address.toProtoObj())
        cellProto.displayValue = self.displayValue
        cellProto.value = str(self.bareValue)
        cellProto.script = default(self.__script, "")
        cellProto.formula = default(self.__formula, "")
        cellProto.isObject = type(self.__value) not in DataCell.texualType
        return cellProto

    @property
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
        if isinstance(self.__value, Exception):
            return convertExceptionToStr(self.__value)
        else:
            if self.__value is None:
                return ""
            else:
                return str(self.__value)

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
                translator = self.__translatorGetter()
                if translator is not None:
                    newScript = self._translateFormula(self.formula, translator)
                    self.__script = newScript
        return self.__script

    @script.setter
    def script(self, newScript: str):
        if newScript!= self.__script:
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
            sameScript = self.script == other.script or (not(self.script and other.script))
            sameAddress = self.address == other.address
            return sameValue and sameScript and sameAddress
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
        self.__value = anotherCell.bareValue
        self.__formula = anotherCell.bareFormula
        self.__script = anotherCell.bareScript
