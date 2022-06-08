from typing import Callable

from com.emeraldblast.p6.document_structure.cell.util.CellUtils import CellUtils
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateRequest import \
    CellUpdateRequest
from com.emeraldblast.p6.document_structure.communication.event.data_structure.cell_event.CellUpdateResponse import \
    CellUpdateResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.WorkbookUpdateCommonResponse import \
    WorkbookUpdateCommonResponse
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class CellUpdateReactor(EventReactor[bytes, WorkbookUpdateCommonResponse]):

    def __init__(self, uid: str, wbGetter: Callable[[WorkbookKey | str | int], Result[Workbook, ErrorReport]]):
        self._id = uid
        self._wbGetter = wbGetter

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: bytes) -> WorkbookUpdateCommonResponse:
        request = CellUpdateRequest.fromProtoBytes(data)
        cellAddress = request.cellAddress
        getWbRs = self._wbGetter(request.workbookKey)
        if getWbRs.isOk():
            wb: Workbook = getWbRs.value.rootWorkbook
            getWsRs = wb.getWorksheetRs(request.worksheetName)
            if getWsRs.isOk():
                ws = getWsRs.value
                cell = ws.cell(cellAddress)
                if request.isNotEmpty():
                    if request.value:
                        cell.value = CellUtils.parseValue(request.value)
                    if request.formula:
                        cell.formula = request.formula
                else:
                    ws.deleteCell(cellAddress)
                wb.reRun()
                rt= CellUpdateResponse(
                    isError = False,
                    workbookKey = request.workbookKey,
                    newWorkbook = wb)
                return rt

            else:
                rt= CellUpdateResponse(
                    workbookKey = request.workbookKey,
                    newWorkbook = None,
                    isError = True,
                    errorReport = getWsRs.err
                )
                rt.errorReport.loc = "CellUpdateReactor"
                return rt
        else:
            rt= CellUpdateResponse(
                workbookKey = request.workbookKey,
                newWorkbook = None,
                isError = True,
                errorReport = getWbRs.err
            )
            rt.errorReport.loc = "CellUpdateReactor"
            return rt
