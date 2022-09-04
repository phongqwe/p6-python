from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMultiRequest import \
     DeleteMultiRequest
from com.qxdzbc.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMultiResponse import \
    DeleteMultiResponse
from com.qxdzbc.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter
from com.qxdzbc.p6.document_structure.communication.reactor.BaseEventReactor import BaseEventReactor
from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
from com.qxdzbc.p6.document_structure.worksheet.Worksheet import Worksheet


class DeleteMultiReactor(BaseEventReactor[bytes, DeleteMultiResponse]):

    def __init__(self, wbGetter: WbGetter):
        super().__init__()
        self._wbGetter = wbGetter

    def react(self, data: bytes) -> DeleteMultiResponse:
        request = DeleteMultiRequest.fromProtoBytes(data)
        wbKey = request.workbookKey
        getWbRs = self._wbGetter(wbKey)
        rt = DeleteMultiResponse(
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
                rt.errorReport.loc = "DeleteMultiReactor"
        else:
            rt.isError = True
            rt.errorReport = getWbRs.err
            rt.errorReport.loc = "DeleteMultiReactor"

        return rt
