from typing import TypeAlias, Callable

from com.qxdzbc.p6.document_structure.app.App import App
from com.qxdzbc.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.qxdzbc.p6.document_structure.range.Range import Range
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet

RangeGetter: TypeAlias = Callable[[RangeId],Result[Range,ErrorReport]]
WsGetter: TypeAlias = Callable[[WorkbookKey,str],Result[Worksheet,ErrorReport]]
WbGetter: TypeAlias = Callable[[WorkbookKey | str | int], Result[Workbook, ErrorReport]]
AppGetter: TypeAlias = Callable[[],App]