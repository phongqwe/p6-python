from typing import TypeAlias, Callable

from com.emeraldblast.p6.document_structure.app.App import App
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey

WbGetter: TypeAlias = Callable[[WorkbookKey | str | int], Result[Workbook, ErrorReport]]
AppGetter: TypeAlias = Callable[[],App]