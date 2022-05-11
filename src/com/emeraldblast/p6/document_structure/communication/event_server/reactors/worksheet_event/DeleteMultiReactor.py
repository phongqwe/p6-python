from com.emeraldblast.p6.document_structure.communication.event.data_structure.workbook_event.WorkbookUpdateCommonResponse import \
    WorkbookUpdateCommonResponse
from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMulti import \
     DeleteMultiRequest
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter
from com.emeraldblast.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor, I, O
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class DeleteMultiReactor(BaseEventReactor[bytes, WorkbookUpdateCommonResponse]):

    def __init__(self, wbGetter: WbGetter):
        super().__init__()
        self._wbGetter = wbGetter

    def react(self, data: bytes) -> WorkbookUpdateCommonResponse:
        request = DeleteMultiRequest.fromProtoBytes(data)
        wbKey = request.workbookKey
        getWbRs = self._wbGetter(wbKey)
        rt = WorkbookUpdateCommonResponse(
            isError = False,
            workbookKey = wbKey,
        )

        if getWbRs.isOk():
            wb: Workbook = getWbRs.value
            getWsRs = wb.getWorksheetRs(request.worksheetName)
            if getWsRs.isOk():
                ws: Worksheet = getWsRs.value
                for cellAddress in request.cellList:
                    ws.deleteCell(cellAddress)
                for rangeAddress in request.rangeList:
                    ws.deleteRange(rangeAddress)
                rt.isError = False
                wb.reRun()
                rt.newWorkbook = wb
            else:
                rt.isError = True
                rt.errorReport = getWsRs.err
        else:
            rt.isError = True
            rt.errorReport = getWbRs.err

        return rt
