from com.qxdzbc.p6.range.Range import Range
from com.qxdzbc.p6.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey


class RpcRange(Range):
    def __init__(self, rangeAddress:RangeAddress, wbKey:WorkbookKey, wsName:str):
        self._address = rangeAddress
        self._wbk = wbKey
        self._wsName = wsName