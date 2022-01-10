from bicp_document_structure.app.GlobalScope import getGlobals
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.CellJson import CellJson
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.cell.util.CellUtil import convertExceptionToStr
from bicp_document_structure.code_executor.CodeExecutor import CodeExecutor


class DataCell(Cell):
    """
    a cell that holds some data
    """

    def __init__(self, address: CellAddress, value=None, code: str = ""):
        self.__value = value
        self.__code: str = code
        self.__addr:CellAddress = address


    ### >> Cell << ###
    def toJson(self) -> CellJson:
        return CellJson(
            value=str(self.value),
            code=self.script,
            address=self.__addr.toJson(),
        )

    def _bareValue(self):
        return self.__value

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
            self.runScript(getGlobals())
        return self.__value

    @value.setter
    def value(self, newValue):
        self.__value = newValue

    @property
    def script(self) -> str:
        return self.__code

    @script.setter
    def script(self, newCode: str):
        self.__code = newCode

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
