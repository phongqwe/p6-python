from com.qxdzbc.p6.document_structure.cell.Cell import Cell
from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.new_architecture.rpc.data_structure.CellValue import CellValue


class RpcCell(Cell):
    @property
    def address(self) -> CellAddress:
        return self._address

    def __init__(self,cellAddress:CellAddress,wbKey:WorkbookKey,wsName:str):
        self._address=cellAddress
        self._wbk = wbKey
        self._wsName = wsName

    @property
    def cellValue(self) -> CellValue:
        cellValue = CellValue()
        cell = self
        if isinstance(cell.bareValue, bool):
            cellValue.bool = cell.bareValue
        if isinstance(cell.bareValue, str):
            cellValue.str = cell.bareValue
        if isinstance(cell.bareValue, int) or isinstance(cell.bareValue, float):
            cellValue.num = cell.bareValue
        return cellValue