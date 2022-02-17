from typing import Callable

from bicp_document_structure.app.GlobalScope import getGlobals
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.util.CellUtil import convertExceptionToStr
from bicp_document_structure.code_executor.CodeExecutor import CodeExecutor
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.P6Events import P6Events
from bicp_document_structure.formula_translator.FormulaTranslators import FormulaTranslators
from bicp_document_structure.util.result.Result import Result


class DataCell(Cell):

    """
    A Cell that holds some data.
    This Cell does not cache value, it perform re-computation on every value request.
    """

    def __init__(self,
                 address: CellAddress,
                 value=None,
                 formula:str=None,
                 script: str = None,
                 onCellChange: Callable[[Cell, P6Event], None] = None):
        self.__value = value
        self.__code: str = script
        self.__addr: CellAddress = address
        self.__onCellChange = onCellChange
        self.__scriptAlreadyRun = False
        self.__formula = formula

    ### >> Cell << ###

    @property
    def formula(self) -> str:
        return self.__formula

    @formula.setter
    def formula(self, newFormula):
        """ set new formula """
        self.__formula = newFormula
        self.script = self.__translateFormula(newFormula)

    @staticmethod
    def __translateFormula(formula:str)->str:
        translator = FormulaTranslators.standard()
        transResult:Result = translator.translate(formula)
        if transResult.isOk():
            return transResult.value
        else:
            raise ValueError(str(transResult.err))


    def bareValue(self):
        return self.__value

    def toJson(self) -> CellJson:
        return CellJson(
            value=self.__value,
            script=self.__code,
            formula=self.__formula,
            address=self.__addr.toJson(),
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
        self.__scriptAlreadyRun=False
        if self.__onCellChange is not None:
            self.__onCellChange(self, P6Events.Cell.UpdateValue)

    @property
    def script(self) -> str:
        return self.__code

    @script.setter
    def script(self, newCode: str):
        self.__code = newCode
        self.__value = None
        if self.__onCellChange is not None:
            self.__onCellChange(self, P6Events.Cell.UpdateScript)
        self.__scriptAlreadyRun = False
        self.__formula = "=SCRIPT({script})".format(script=newCode)

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

    def runScript(self, globalScope=None, localScope=None):
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
            if self.__onCellChange is not None:
                self.__onCellChange(self, P6Events.Cell.UpdateValue)

    def setScriptAndRun(self, newScript, globalScope=None, localScope=None):
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
            if self.__onCellChange is not None:
                self.__onCellChange(self, P6Events.Cell.ClearScriptResult)