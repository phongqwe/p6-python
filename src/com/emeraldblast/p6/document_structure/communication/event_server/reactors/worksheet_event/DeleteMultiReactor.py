from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteMulti import \
    DeleteMultiResponse, DeleteMultiRequest
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor, I, O
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class DeleteMultiReactor(EventReactor[bytes, DeleteMultiResponse]):

    def __init__(self, uid: str, wbGetter: WbGetter):
        self._uid = uid
        self._wbGetter = wbGetter

    @property
    def id(self) -> str:
        return self._uid

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
                rt.newWorkbook = wb

            else:
                rt.isError = True
                rt.errorReport = getWsRs.err
        else:
            rt.isError = True
            rt.errorReport = getWbRs.err

        return rt
