from typing import Any, Callable, Optional

from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.cell.CellContent import CellContent
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.cell.util.CellUtils import convertExceptionToStr, CellUtils
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellId import CellId
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellValue import CellValue
from com.qxdzbc.p6.proto.DocProtos_pb2 import CellProto, CellValueProto


class DataCell(Cell):
    """
    A Cell that holds some data.
    """
    def __init__(self,
                 address: CellAddress,
                 wsName: str,
                 wbKey: WorkbookKey,
                 value: Any = None,
                 formula: str = None,
                 ):
        self._wsName = wsName
        self._wbKey = wbKey
        self.__value: Any = value
        self.__formula: str = formula
        self.__scriptAlreadyRun: bool = False
        self.__addr: CellAddress = address

    @property
    def wsName(self) -> Optional[str]:
        return self._wsName

    @property
    def wbKey(self) -> Optional[WorkbookKey]:
        return self._wbKey

    def isEmpty(self):
        return self.__formula or self.bareValue

    @property
    def cellValue(self) -> CellValue:
        cellValue = CellValue()
        cell = self
        if isinstance(cell.bareValue, bool):
            cellValue.bool = cell.bareValue
        if isinstance(cell.bareValue, str):
            cellValue.vStr = cell.bareValue
        if isinstance(cell.bareValue, int) or isinstance(cell.bareValue, float):
            cellValue.vNum = cell.bareValue
        return cellValue

    @property
    def sourceValue(self) -> str:
        if self.bareFormula:
            return self.bareFormula
        else:
            return self.value

    @property
    def rootCell(self) -> 'Cell':
        return self

    @property
    def content(self) -> CellContent:
        return CellContent(
            value = self.value,
            formula = self.formula,
        )

    @content.setter
    def content(self, newContent: CellContent):
        self.__value = newContent.value
        self.__formula = newContent.formula

    textualType = [int, float, str, bool]

    @property
    def bareScript(self) -> str:
        return self.__script

    @property
    def bareFormula(self) -> str:
        return self.__formula

    @property
    def formula(self) -> str:
        return self.__formula

    @formula.setter
    def formula(self, newFormula):
        self.__formula = newFormula

    def toProtoObj(self) -> CellProto:
        cellProto = CellProto()
        cellProto.address.CopyFrom(self.address.toProtoObj())

        if self.__formula:
            cellProto.formula = self.__formula
        else:
            if self.__value:
                cellValueProto = CellValueProto()
                if isinstance(self.__value, bool):
                    cellValueProto.bool = self.__value
                if isinstance(self.__value, str):
                    cellValueProto.vStr = self.__value
                if isinstance(self.__value, int) or isinstance(self.__value, float):
                    cellValueProto.num = self.__value

                cellProto.value.CopyFrom(cellValueProto)

        return cellProto

    @property
    def bareValue(self):
        return self.__value

    @property
    def displayValue(self) -> str:
        if isinstance(self.__value, Exception):
            return convertExceptionToStr(self.__value)
        else:
            if self.__value is None:
                return ""
            else:
                if isinstance(self.__value, str):
                    if CellUtils.isNumericString(self.__value):
                        return self.__value[1:]
                    else:
                        return self.__value
                else:
                    return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newValue):
        self.__value = newValue
        self.__script = None
        self.__formula = None
        self.__scriptAlreadyRun = False

    def __setScriptWithoutChangingFormula(self, newScript):
        self.__script = newScript
        self.__value = None
        self.__scriptAlreadyRun = False

    @property
    def address(self) -> CellAddress:
        return self.__addr

    def __eq__(self, other):
        if isinstance(other, Cell):
            sameAddress = self.address == other.address
            sameWs = self.wsName == other.wsName
            sameWb = self.wbKey == other.wbKey
            return sameAddress and sameWb and sameWs
        else:
            return False

    @property
    def row(self) -> int:
        return self.__addr.rowIndex

    @property
    def col(self) -> int:
        return self.__addr.colIndex

    def __hash__(self) -> int:
        return hash((self.__addr, self.wsName, self.wbKey))

    def copyFromRs(self, anotherCell: CellId) -> Result[None, ErrorReport]:
        raise TypeError("DataCell does not support copying from CellId")

    def copyFrom(self, anotherCell: CellId):
        raise TypeError("DataCell does not support copying from CellId")

    def copyFromCellRs(self, anotherCell: "Cell") -> Result[None, ErrorReport]:
        if anotherCell.formula:
            self.formula = anotherCell.formula
            return Ok(None)
        if anotherCell.value:
            self.__value = anotherCell.bareValue
            return Ok(None)
