from com.emeraldblast.p6.document_structure.communication.event_server.reactors.TypeAliasForReactor import WbGetter

from com.emeraldblast.p6.document_structure.communication.event.data_structure.worksheet_event.DeleteCell import \
    DeleteCellResponse, DeleteCellRequest
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor, I, O
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet

# TODO test this
class DeleteCellReactor(EventReactor[bytes,DeleteCellResponse]):

    def __init__(self, uid:str,wbGetter: WbGetter):
        self._id = uid
        self._wbGetter = wbGetter

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: bytes) -> DeleteCellResponse:
        request = DeleteCellRequest.fromProtoBytes(data)
        getWbRs = self._wbGetter(request.workbookKey)
        rt = DeleteCellResponse(
            workbookKey = request.workbookKey,
            worksheetName = request.worksheetName,
            cellAddress = request.cellAddress
        )
        if getWbRs.isOk():
            wb:Workbook = getWbRs.value
            getWsRs = wb.getWorksheetRs(request.worksheetName)
            if getWsRs.isOk():
                ws:Worksheet = getWsRs.value
                delRs = ws.deleteCellRs(request.cellAddress)
                if delRs.isOk():
                    wb.reRun()
                    rt.newWorkbook = wb
                else:
                    rt.isError=True
                    rt.errorReport = delRs.err
                    rt.errorReport.loc = "DeleteCellReactor"
            else:
                rt.isError = True
                rt.errorReport = getWsRs.err
                rt.errorReport.loc = "DeleteCellReactor"
        else:
            rt.isError=True
            rt.errorReport = getWbRs.err
            rt.errorReport.loc = "DeleteCellReactor"
        return rt