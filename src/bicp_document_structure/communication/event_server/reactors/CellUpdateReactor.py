from typing import Callable

from bicp_document_structure.communication.event.P6Events import P6Events
from bicp_document_structure.communication.event.reactor.EventReactor import EventReactor, I, O
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey

ResponseClazz = P6Events.Cell.Update.Response
RequestClazz = P6Events.Cell.Update.Request

class CellUpdateReactor(EventReactor[bytes, ResponseClazz]):

    def __init__(self, id:str, wbGetter: Callable[[WorkbookKey | str | int], Result[Workbook, ErrorReport]]):
        self._id = id
        self._wbGetter = wbGetter

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: bytes) -> ResponseClazz:
        request = RequestClazz.fromProtoBytes(data)
        getWbRs = self._wbGetter(request.workbookKey)
        if getWbRs.isOk():
            wb:Workbook = getWbRs.value
            getWsRs = wb.getWorksheetRs(request.worksheetName)
            if getWsRs.isOk():
                ws = getWsRs.value
                cell = ws.cell(request.cellAddress)
                if request.value is not None and len(request.value)>0:
                    cell.value = request.value
                elif request.formula is not None and len(request.formula)>0:
                    cell.formula = request.formula
                else:
                    pass # do nothing

                return ResponseClazz(
                    newWorkbook = wb
                )

            else:
                return ResponseClazz(
                    newWorkbook = None,
                    isError = True,
                    errorReport = getWsRs.err
                )
        else:
            return ResponseClazz(
                newWorkbook = None,
                isError = True,
                errorReport = getWbRs.err
            )