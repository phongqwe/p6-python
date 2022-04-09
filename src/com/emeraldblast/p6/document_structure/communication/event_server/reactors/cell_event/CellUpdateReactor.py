from typing import Callable

from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateCommonResponse import \
    CellUpdateCommonResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateRequest import \
    CellUpdateRequest
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class CellUpdateReactor(EventReactor[bytes, CellUpdateCommonResponse]):

    def __init__(self, uid: str, wbGetter: Callable[[WorkbookKey | str | int], Result[Workbook, ErrorReport]]):
        self._id = uid
        self._wbGetter = wbGetter

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: bytes) -> CellUpdateCommonResponse:
        request = CellUpdateRequest.fromProtoBytes(data)
        cellAddress = request.cellAddress
        getWbRs = self._wbGetter(request.workbookKey)
        if getWbRs.isOk():
            wb: Workbook = getWbRs.value
            getWsRs = wb.getWorksheetRs(request.worksheetName)
            if getWsRs.isOk():
                ws = getWsRs.value
                cell = ws.cell(cellAddress)
                if request.isNotEmpty():
                    if request.value is not None and len(request.value) > 0:
                        cell.value = request.value
                    elif request.formula is not None and len(request.formula) > 0:
                        cell.formula = request.formula
                    else:
                        pass  # do nothing
                else:
                    ws.deleteCell(cellAddress)
                wb.reRun()
                return CellUpdateCommonResponse(
                    workbookKey = request.workbookKey,
                    newWorkbook = wb)

            else:
                return CellUpdateCommonResponse(
                    workbookKey = request.workbookKey,
                    newWorkbook = None,
                    isError = True,
                    errorReport = getWsRs.err
                )
        else:
            return CellUpdateCommonResponse(
                workbookKey = request.workbookKey,
                newWorkbook = None,
                isError = True,
                errorReport = getWbRs.err
            )
