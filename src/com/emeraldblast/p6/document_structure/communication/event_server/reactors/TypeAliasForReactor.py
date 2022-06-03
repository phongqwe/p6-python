from typing import TypeAlias, Callable

from com.emeraldblast.p6.document_structure.app.App import App
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeId import RangeId
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet

RangeGetter: TypeAlias = Callable[[RangeId],Result[Range,ErrorReport]]
WsGetter: TypeAlias = Callable[[WorkbookKey,str],Result[Worksheet,ErrorReport]]
WbGetter: TypeAlias = Callable[[WorkbookKey | str | int], Result[Workbook, ErrorReport]]
AppGetter: TypeAlias = Callable[[],App]