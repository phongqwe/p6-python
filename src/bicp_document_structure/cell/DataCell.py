from typing import Callable

from bicp_document_structure.app.GlobalScope import getGlobals
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.util.CellUtil import convertExceptionToStr
from bicp_document_structure.code_executor.CodeExecutor import CodeExecutor
from bicp_document_structure.mutation.CellMutationEvent import CellMutationEvent


class DataCell(Cell):
    """
    a cell that holds some data
    """

    def bareValue(self):
        return self.__value

    def __init__(self,
                 address: CellAddress,
                 value=None,
                 code: str = "",
                 onCellMutation:Callable[[CellAddress,CellMutationEvent],None] = None):
        self.__value = value
        self.__code: str = code
        self.__addr:CellAddress = address
        self.__onCelMutation = onCellMutation


    ### >> Cell << ###
    def toJson(self) -> CellJson:
        return CellJson(
            value=str(self.__value),
            script=self.__code,
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
        get the value contained in this cell. If this cell contains code, the code will run and the updated value will be returned
        """
        if self.hasCode():
            # x: this will update self.__value
            self.runScript(getGlobals())
        return self.__value

    @value.setter
    def value(self, newValue):
        self.__value = newValue
        if self.__onCelMutation is not None:
            self.__onCelMutation(self.address,CellMutationEvent.NEW_VALUE)

    @property
    def script(self) -> str:
        return self.__code

    @script.setter
    def script(self, newCode: str):
        self.__code = newCode
        if self.__onCelMutation is not None:
            self.__onCelMutation(self.address, CellMutationEvent.NEW_SCRIPT)

    @property
    def address(self) -> CellAddress:
        return self.__addr

    def isValueEqual(self, anotherCell):
        return self.value == anotherCell.value

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
        if localScope is None:
            localScope = {}

        if globalScope is None:
            globalScope = getGlobals()
        try:
            codeResult = CodeExecutor.evalCode(self.script, globalScope, localScope)
        except Exception as e:
            codeResult = e
        self.value = codeResult

    def setScriptAndRun(self, newScript, globalScope=None, localScope=None):
        self.script = newScript
        self.runScript(globalScope, localScope)

    def hasCode(self) -> bool:
        return self.__code is not None and len(self.__code) != 0

    def __hash__(self) -> int:
        return hash((self.__value,self.__code,self.__addr))