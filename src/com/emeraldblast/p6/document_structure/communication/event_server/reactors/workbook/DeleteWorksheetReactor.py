from com.emeraldblast.p6.document_structure.communication.event.data.request.DeleteWorksheetRequest import \
    DeleteWorksheetRequest
from com.emeraldblast.p6.document_structure.communication.event.data.response.DeleteWorksheetResponse import \
    DeleteWorksheetResponse
from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook


class DeleteWorksheetReactor(EventReactor[bytes, DeleteWorksheetResponse]):

    def __init__(self, id: str, wbGetter: WbGetter):
        self._id = id
        self._wbGetter = wbGetter

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: bytes) -> DeleteWorksheetResponse:
        request: DeleteWorksheetRequest = DeleteWorksheetRequest.fromProtoBytes(data)
        wbRs = self._wbGetter(request.workbookKey)
        rt = DeleteWorksheetResponse(
            workbookKey = request.workbookKey,
            targetWorksheetList = request.targetWorksheet,
        )
        if wbRs.isOk():
            wb: Workbook = wbRs.value
            deleteRs = wb.deleteWorksheetRs(request.targetWorksheet)
            if deleteRs.isOk():
                rt.isError = False
                return rt
            else:
                rt.isError = True
                rt.errorReport = deleteRs.err
                return rt
        else:
            rt.isError = True
            rt.errorReport = wbRs.err
            return rt
